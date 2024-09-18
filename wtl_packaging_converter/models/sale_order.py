# -*- coding: utf-8 -*-

from odoo import fields, models, api, _

class SaleOrderLine(models.Model):
    _inherit = "sale.order.line"

    boxes_id = fields.Float(string="Cajas")
    tabletas_id = fields.Float(string="Tabletas")
    blister_id = fields.Float(string="Blister")

    #Este metodo checa de que tipo de UOM es el producto, y suma las cajas y tabletas que se coloquen
    @api.onchange('boxes_id', 'tabletas_id', 'product_uom', 'blister_id')
    def _onchange_boxes_id_and_tabletas_id(self):
        for line in self:
            if line.product_id and line.boxes_id > 0 or line.tabletas_id > 0 or line.blister_id > 0:
                if line.product_uom.is_unit:
                    if line.boxes_id > 0 or line.tabletas_id > 0 or line.blister_id > 0:
                        cajas = line.boxes_id * line.product_id.qty_for_box
                        tabletas = line.tabletas_id / line.product_id.qty_for_box
                        blister_a_tableta = line.blister_id * line.product_id.qty_for_blister
                        blister = blister_a_tableta / line.product_id.qty_for_box
                        line.product_uom_qty = cajas + tabletas + blister
                else:
                    if line.boxes_id > 0 or line.tabletas_id > 0 or line.blister_id > 0:
                        cajas = line.boxes_id
                        tabletas = line.tabletas_id / line.product_id.qty_for_box
                        blister_a_tableta = line.blister_id * line.product_id.qty_for_blister
                        blister = blister_a_tableta / line.product_id.qty_for_box
                        line.product_uom_qty = cajas + tabletas + blister
            else:
                line.product_qty = 0