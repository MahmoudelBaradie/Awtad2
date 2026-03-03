from odoo import api, fields, models, _
from odoo.exceptions import UserError


class RealEstateProject(models.Model):
    _name='real.estate.project'
    _inherit=['mail.thread']
    _description='Real Estate Project'

    name=fields.Char(default='New', required=True)
    land_id=fields.Many2one('real.estate.land', required=True)
    estimated_budget=fields.Monetary(required=True)
    actual_cost=fields.Monetary(compute='_compute_actual', store=True)
    variance=fields.Monetary(compute='_compute_actual', store=True)
    state=fields.Selection([('draft','Draft'),('in_progress','In Progress'),('completed','Completed'),('closed','Closed')], default='draft', tracking=True)
    close_mode=fields.Selection([('inventory','Inventory Units'),('investment','Investment Property')])
    currency_id=fields.Many2one('res.currency',default=lambda self:self.env.company.currency_id)
    analytic_account_id=fields.Many2one('account.analytic.account',readonly=True)
    cost_line_ids=fields.One2many('real.estate.project.cost','project_id')


    @api.model_create_multi
    def create(self, vals_list):
        for vals in vals_list:

            if vals.get('name','New')=='New':
                vals['name']=self.env['ir.sequence'].next_by_code('real.estate.project') or 'New'
        recs=super().create(vals_list)
        plan=self.env.ref('analytic.analytic_plan_projects')
        for rec in recs:
            rec.analytic_account_id=self.env['account.analytic.account'].create({'name':rec.name,'plan_id':plan.id}).id
        return recs

    @api.depends('cost_line_ids.amount','estimated_budget')
    def _compute_actual(self):
        for rec in self:
            rec.actual_cost=sum(rec.cost_line_ids.mapped('amount'))
            rec.variance=rec.estimated_budget-rec.actual_cost

    def action_start(self): self.write({'state':'in_progress'})
    def action_complete(self): self.write({'state':'completed'})

    def action_close_project(self):
        config=self.env['real.estate.company.config'].search([('company_id','=',self.env.company.id)],limit=1)
        if not config:
            raise UserError(_('Missing accounting configuration.'))
        for rec in self:
            if rec.close_mode not in ('inventory','investment'):
                raise UserError(_('Please select conversion mode.'))
            debit_account=config.inventory_account_id if rec.close_mode=='inventory' else config.investment_property_account_id
            move=self.env['account.move'].create({'move_type':'entry','journal_id':config.default_journal_id.id,'line_ids':[
                (0,0,{'name':rec.name,'account_id':debit_account.id,'debit':rec.actual_cost,'credit':0}),
                (0,0,{'name':rec.name,'account_id':config.wip_account_id.id,'debit':0,'credit':rec.actual_cost}),
            ]})
            move.action_post()
            rec.state='closed'

class RealEstateProjectCost(models.Model):
    _name='real.estate.project.cost'
    _description='Project Cost Line'
    project_id=fields.Many2one('real.estate.project',required=True,ondelete='cascade')
    category=fields.Selection([('foundations','Foundations'),('concrete','Concrete'),('steel','Steel'),('finishing','Finishing'),('marble','Marble'),('equipment','Equipment'),('consultancy','Consultancy'),('other','Other')],required=True)
    amount=fields.Monetary(required=True)
    bill_id=fields.Many2one('account.move',domain=[('move_type','=','in_invoice')])
    currency_id=fields.Many2one(related='project_id.currency_id',store=True)

    @api.model_create_multi
    def create(self, vals_list):
        records=super().create(vals_list)
        config=self.env['real.estate.company.config'].search([('company_id','=',self.env.company.id)],limit=1)
        for rec in records:
            move=self.env['account.move'].create({'move_type':'entry','journal_id':config.default_journal_id.id,'line_ids':[
                (0,0,{'name':rec.project_id.name,'account_id':config.wip_account_id.id,'debit':rec.amount,'credit':0,'analytic_distribution':{str(rec.project_id.analytic_account_id.id):100}}),
                (0,0,{'name':rec.project_id.name,'account_id':config.retention_payable_account_id.id,'debit':0,'credit':rec.amount}),

            ]})
            move.action_post()
        return records
