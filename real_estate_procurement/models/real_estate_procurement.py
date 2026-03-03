from odoo import api, fields, models


class RealEstateContractorContract(models.Model):
    _name = 'real.estate.contractor.contract'
    _inherit = 'real.estate.accounting.mixin'
    _description = 'Contractor Contract'

    name = fields.Char(required=True, default='New')
    partner_id = fields.Many2one('res.partner', required=True)
    project_id = fields.Many2one('real.estate.project', required=True)
    contract_value = fields.Monetary(required=True)
    retention_percentage = fields.Float(default=10.0)
    billed_amount = fields.Monetary()
    state = fields.Selection([('draft', 'Draft'), ('active', 'Active'), ('done', 'Done')], default='draft')
    currency_id = fields.Many2one('res.currency', default=lambda self: self.env.company.currency_id)

    @api.model_create_multi
    def create(self, vals_list):
        for vals in vals_list:
            if vals.get('name', 'New') == 'New':
                vals['name'] = self.env['ir.sequence'].next_by_code('real.estate.contractor.contract') or 'New'
        return super().create(vals_list)

    def action_progress_bill(self):
        config = self._get_re_company_config()
        for rec in self:
            retention = rec.contract_value * rec.retention_percentage / 100
            payable = rec.contract_value - retention
            move = self.env['account.move'].create({'move_type': 'entry', 'journal_id': config.default_journal_id.id, 'line_ids': [
                (0, 0, {'name': rec.name, 'account_id': config.wip_account_id.id, 'debit': rec.contract_value, 'credit': 0, 'analytic_distribution': {str(rec.project_id.analytic_account_id.id): 100}}),
                (0, 0, {'name': rec.name, 'account_id': config.retention_payable_account_id.id, 'debit': 0, 'credit': retention}),
                (0, 0, {'name': rec.name, 'account_id': config.payable_account_id.id, 'debit': 0, 'credit': payable}),
            ]})
            move.action_post()
            rec.billed_amount += rec.contract_value
            rec.state = 'active'
