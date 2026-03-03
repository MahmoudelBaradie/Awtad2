from odoo import fields, models

class RealEstatePropertyAsset(models.Model):
    _name='real.estate.property.asset'
    _description='Investment Property Asset'

    name=fields.Char(required=True)
    unit_id=fields.Many2one('real.estate.unit', required=True)
    acquisition_cost=fields.Monetary(required=True)
    useful_life_years=fields.Integer(default=20)
    monthly_depreciation=fields.Monetary(compute='_compute_dep')
    currency_id=fields.Many2one('res.currency',default=lambda self:self.env.company.currency_id)

    def _compute_dep(self):
        for rec in self:
            rec.monthly_depreciation=(rec.acquisition_cost/(rec.useful_life_years*12)) if rec.useful_life_years else 0
