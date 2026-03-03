from odoo import api, fields, models

class RealEstateUnit(models.Model):
    _name='real.estate.unit'
    _description='Real Estate Unit'

    name=fields.Char(default='New', required=True)
    project_id=fields.Many2one('real.estate.project', required=True)
    unit_type=fields.Selection([('apartment','Apartment'),('villa','Villa'),('office','Office'),('shop','Shop')], required=True)
    area=fields.Float(required=True)
    cost=fields.Monetary(required=True)
    target_price=fields.Monetary(required=True)
    status=fields.Selection([('available','Available'),('reserved','Reserved'),('sold','Sold'),('rented','Rented')], default='available')
    currency_id=fields.Many2one('res.currency',default=lambda self:self.env.company.currency_id)
    margin=fields.Monetary(compute='_compute_margin')

    @api.depends('target_price','cost')
    def _compute_margin(self):
        for rec in self:
            rec.margin=rec.target_price-rec.cost

    @api.model_create_multi
    def create(self, vals_list):
        for vals in vals_list:
            if vals.get('name','New')=='New':
                vals['name']=self.env['ir.sequence'].next_by_code('real.estate.unit') or 'New'
        return super().create(vals_list)
