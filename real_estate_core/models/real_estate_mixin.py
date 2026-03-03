from odoo import _, models
from odoo.exceptions import UserError


class RealEstateAccountingMixin(models.AbstractModel):
    _name = 'real.estate.accounting.mixin'
    _description = 'Real Estate Accounting/Analytic Helper Mixin'

    def _get_re_company_config(self, company=None):
        company = company or self.env.company
        config = self.env['real.estate.company.config'].search([
            ('company_id', '=', company.id),
        ], limit=1)
        if not config:
            raise UserError(_('Please configure Real Estate accounting accounts first for %s.') % company.display_name)
        return config

    def _get_re_analytic_plan(self):
        plan = self.env.ref('analytic.analytic_plan_projects', raise_if_not_found=False)
        if not plan:
            plan = self.env['account.analytic.plan'].search([], limit=1)
        if not plan:
            raise UserError(_('No analytic plan found. Please create one before using real estate modules.'))
        return plan
