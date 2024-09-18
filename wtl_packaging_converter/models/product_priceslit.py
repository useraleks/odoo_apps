# -*- coding: utf-8 -*-

from odoo import fields, models, api, _

class ProductPricelist(models.Model):
    _inherit = "product.pricelist"


class ProductPricelistItem(models.Model):
    _inherit = "product.pricelist.item"

    min_qty_x_package = fields.Boolean(string="Aplicar precio minipo por empaquetado?")
    caja_id = fields.Float(string="Caja")
    blister_id = fields.Float(string="Blister")
    tableta_id = fields.Float(string="Tableta")

    #Este metodo checa de que tipo de UOM es el producto, y suma las cajas y tabletas que se coloquen
    @api.onchange('caja_id', 'blister_id', 'tableta_id')
    def _onchange_caja_and_blister_and_tableta(self):
        for line in self:
            if line.product_tmpl_id and line.caja_id > 0 or line.blister_id > 0 or line.tableta_id > 0:
                if line.product_tmpl_id.uom_id.is_unit:
                    if line.caja_id > 0 or line.blister_id > 0 or line.tableta_id > 0:
                        cajas = line.caja_id * line.product_tmpl_id.qty_for_box
                        tabletas = line.tableta_id / line.product_tmpl_id.qty_for_box
                        line.min_quantity = cajas + tabletas
                else:
                    if line.caja_id > 0 or line.blister_id > 0 or line.tableta_id > 0:
                        cajas = line.caja_id
                        tabletas = line.tableta_id / line.product_tmpl_id.qty_for_box
                        line.min_quantity = cajas + tabletas
            else:
                line.min_quantity = 0