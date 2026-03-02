from odoo import fields, models


class RealEstateCompanyConfig(models.Model):
    _name = 'real.estate.company.config'
    _description = 'Real Estate Accounting Configuration'

    company_id = fields.Many2one('res.company', required=True, default=lambda self: self.env.company)
    land_asset_account_id = fields.Many2one('account.account', required=True)
    wip_account_id = fields.Many2one('account.account', required=True)
    inventory_account_id = fields.Many2one('account.account', required=True)
    investment_property_account_id = fields.Many2one('account.account', required=True)
    cost_of_sales_account_id = fields.Many2one('account.account', required=True)
    sales_revenue_account_id = fields.Many2one('account.account', required=True)
    rental_revenue_account_id = fields.Many2one('account.account', required=True)
    security_deposit_account_id = fields.Many2one('account.account', required=True)
    retention_payable_account_id = fields.Many2one('account.account', required=True)
    cash_account_id = fields.Many2one('account.account', required=True)
    bank_account_id = fields.Many2one('account.account', required=True)
    payable_account_id = fields.Many2one('account.account', required=True)
    receivable_account_id = fields.Many2one('account.account', required=True)
    default_journal_id = fields.Many2one('account.journal', required=True, domain=[('type', '=', 'general')])

    _sql_constraints = [
        ('company_unique', 'unique(company_id)', 'Only one configuration is allowed per company.'),
    ]
