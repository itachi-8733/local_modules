# -*- coding: utf-8 -*-

from odoo import models, fields, api, _
from odoo.exceptions import UserError


class ProductTemplate(models.Model):
    _inherit = 'product.template'

    discount_percentage = fields.Float('Discount Percentage')
    discount_amount = fields.Float('Discount Amount', compute='get_disc_amt')

    @api.depends('discount_percentage')
    def get_disc_amt(self):
        for rec in self:
            rec.discount_amount = rec.list_price * (1 - rec.discount_percentage / 100)

    @api.constrains('discount_percentage')
    def _check_percentage(self):
        if (self.discount_percentage >= 100) and (self.discount_percentage <= 0):
            raise UserError("discount percentage cannot be less than 0 or greater than 100")

    def _get_sales_prices(self, website):
        res = super(ProductTemplate, self)._get_sales_prices(website)
        for template in self:
            res.get(template.id).update({
                'custom_percentage': template.discount_percentage,
                'custom_price': template.discount_amount
            })
        return res

