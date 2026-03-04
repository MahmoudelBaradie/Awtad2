from odoo import api, fields, models


class RealEstateRental(models.Model):
    _name = 'real.estate.rental'
    _inherit = 'real.estate.accounting.mixin'
    _description = 'Rental Contract'

    name = fields.Char(required=True, default='New')
    tenant_id = fields.Many2one('res.partner', required=True)
    unit_id = fields.Many2one('real.estate.unit', required=True, domain=[('status', '=', 'available')])
    date_start = fields.Date(required=True)
    date_end = fields.Date(required=True)
    rent_value = fields.Monetary(required=True)
    billing_cycle = fields.Selection([('monthly', 'Monthly'), ('quarterly', 'Quarterly')], default='monthly')
    security_deposit = fields.Monetary()
    state = fields.Selection([('draft', 'Draft'), ('active', 'Active'), ('closed', 'Closed')], default='draft')
    currency_id = fields.Many2one('res.currency', default=lambda self: self.env.company.currency_id)

    @api.model_create_multi
    def create(self, vals_list):
        for vals in vals_list:
            if vals.get('name', 'New') == 'New':
                vals['name'] = self.env['ir.sequence'].next_by_code('real.estate.rental') or 'New'
        return super().create(vals_list)

    def action_activate(self):
        for rec in self:
            rec.state = 'active'
            rec.unit_id.status = 'rented'

    def action_close(self):
        for rec in self:
            rec.state = 'closed'
            rec.unit_id.status = 'available'

    def cron_generate_rent_entries(self):
        config = self._get_re_company_config()
        for rec in self.search([('state', '=', 'active')]):
            move = self.env['account.move'].create({'move_type': 'entry', 'journal_id': config.default_journal_id.id, 'line_ids': [
                (0, 0, {'name': rec.name, 'account_id': config.receivable_account_id.id, 'debit': rec.rent_value, 'credit': 0}),
                (0, 0, {'name': rec.name, 'account_id': config.rental_revenue_account_id.id, 'debit': 0, 'credit': rec.rent_value}),
            ]})
            move.action_post()
