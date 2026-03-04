from odoo import api, fields, models, _
from odoo.exceptions import UserError


class RealEstateLand(models.Model):
    _name = 'real.estate.land'
    _inherit = ['real.estate.accounting.mixin', 'mail.thread', 'mail.activity.mixin']
    _description = 'Real Estate Land'

    name = fields.Char(default='New', tracking=True)
    location = fields.Char(required=True)
    area = fields.Float(required=True)
    area_uom = fields.Selection([('feddan', 'Feddan'), ('qirat', 'Qirat'), ('sqm', 'Sqm')], default='sqm', required=True)
    area_sqm = fields.Float(compute='_compute_area_sqm', store=True)
    purchase_price = fields.Monetary(required=True)
    additional_cost = fields.Monetary()
    total_land_cost = fields.Monetary(compute='_compute_total_cost', store=True)
    payment_method = fields.Selection([('cash', 'Cash'), ('bank', 'Bank'), ('payable', 'Payable')], required=True)
    state = fields.Selection([('draft', 'Draft'), ('confirmed', 'Confirmed'), ('capitalized', 'Capitalized')], default='draft', tracking=True)
    currency_id = fields.Many2one('res.currency', default=lambda self: self.env.company.currency_id)
    analytic_account_id = fields.Many2one('account.analytic.account', readonly=True)
    move_id = fields.Many2one('account.move', readonly=True)

    @api.model_create_multi
    def create(self, vals_list):
        for vals in vals_list:
            if vals.get('name', 'New') == 'New':
                vals['name'] = self.env['ir.sequence'].next_by_code('real.estate.land') or 'New'
        return super().create(vals_list)

    @api.depends('purchase_price', 'additional_cost')
    def _compute_total_cost(self):
        for rec in self:
            rec.total_land_cost = rec.purchase_price + rec.additional_cost

    @api.depends('area', 'area_uom')
    def _compute_area_sqm(self):
        factor = {'sqm': 1, 'qirat': 175.0, 'feddan': 4200.0}
        for rec in self:
            rec.area_sqm = rec.area * factor.get(rec.area_uom, 1)

    def action_confirm(self):
        for rec in self.filtered(lambda r: r.state == 'draft'):
            config = rec._get_re_company_config()
            if not rec.analytic_account_id:
                plan = rec._get_re_analytic_plan()
                rec.analytic_account_id = self.env['account.analytic.account'].create({'name': rec.name, 'plan_id': plan.id}).id

            credit_account = {
                'cash': config.cash_account_id.id,
                'bank': config.bank_account_id.id,
                'payable': config.payable_account_id.id,
            }.get(rec.payment_method)
            if not credit_account:
                raise UserError(_('Please select a valid payment method.'))

            line_vals = [
                (0, 0, {'name': rec.name, 'account_id': config.land_asset_account_id.id, 'debit': rec.total_land_cost, 'credit': 0.0, 'analytic_distribution': {str(rec.analytic_account_id.id): 100}}),
                (0, 0, {'name': rec.name, 'account_id': credit_account, 'debit': 0.0, 'credit': rec.total_land_cost}),
            ]
            rec.move_id = self.env['account.move'].create({'move_type': 'entry', 'journal_id': config.default_journal_id.id, 'line_ids': line_vals}).id
            rec.move_id.action_post()
            rec.state = 'confirmed'

    def action_capitalize(self):
        self.write({'state': 'capitalized'})

    def write(self, vals):
        if any(rec.state == 'capitalized' for rec in self):
            allowed = {'message_follower_ids', 'activity_ids'}
            if not set(vals).issubset(allowed):
                raise UserError(_('Capitalized land cannot be modified.'))
        return super().write(vals)
