
from odoo import fields, models, _
from odoo.exceptions import UserError

class RealEstateSale(models.Model):
    _name='real.estate.sale'
    _inherit=['mail.thread']
    _description='Unit Sales Contract'

    name=fields.Char(required=True, default='New')
    partner_id=fields.Many2one('res.partner', required=True)
    unit_id=fields.Many2one('real.estate.unit', required=True, domain=[('status','in',['available','reserved'])])
    contract_date=fields.Date(default=fields.Date.today)
    sale_price=fields.Monetary(required=True)
    down_payment=fields.Monetary()
    delivery_status=fields.Selection([('pending','Pending'),('delivered','Delivered')], default='pending')
    state=fields.Selection([('draft','Draft'),('reserved','Reserved'),('contracted','Contracted'),('posted','Posted')],default='draft',tracking=True)
    currency_id=fields.Many2one('res.currency', default=lambda self:self.env.company.currency_id)
    margin=fields.Monetary(compute='_compute_margin')

    def _compute_margin(self):
        for rec in self:
            rec.margin=rec.sale_price-rec.unit_id.cost

    def _config(self):
        config=self.env['real.estate.company.config'].search([('company_id','=',self.env.company.id)],limit=1)
        if not config:
            raise UserError(_('Missing accounting bridge configuration'))
        return config

    def action_reserve(self):
        self.write({'state':'reserved'})
        self.unit_id.status='reserved'

    def action_contract(self):
        self.write({'state':'contracted'})

    def action_post_sale(self):
        config=self._config()
        for rec in self:
            move=self.env['account.move'].create({'move_type':'entry','journal_id':config.default_journal_id.id,'line_ids':[
                (0,0,{'name':rec.name,'account_id':config.cost_of_sales_account_id.id,'debit':rec.unit_id.cost,'credit':0}),
                (0,0,{'name':rec.name,'account_id':config.inventory_account_id.id,'debit':0,'credit':rec.unit_id.cost}),
                (0,0,{'name':rec.name,'account_id':config.receivable_account_id.id,'debit':rec.sale_price,'credit':0}),
                (0,0,{'name':rec.name,'account_id':config.sales_revenue_account_id.id,'debit':0,'credit':rec.sale_price}),
            ]})
            move.action_post()
            rec.state='posted'
            rec.unit_id.status='sold'
