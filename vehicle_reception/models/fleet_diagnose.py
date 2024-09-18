# -*- coding: utf-8 -*-

from odoo import models, fields, api

class SparePartLine(models.Model):
    _inherit = 'spare.part.line'
    
    product_id = fields.Many2one('product.template', string='Product', required=True)
    
    @api.onchange('product_id')
    def onchange_product_id(self):
        res = {}
        product_obj = self.env['product.template']
        if self.product_id:
            res = {'default_code': self.product_id.default_code,'price_unit': self.product_id.list_price}
        return {'value': res}