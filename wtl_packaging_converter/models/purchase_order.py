# -*- coding: utf-8 -*-

from odoo import fields, models, api, _

class PurchaseOrderLine(models.Model):
    _inherit = "purchase.order.line"

    boxes_id = fields.Float(string="Cajas")

    @api.onchange('boxes_id')
    def _onchange_boxes_id(self):
        for line in self:
            if line.product_id and line.boxes_id > 0:
                if line.product_uom.is_unit:
                    if line.boxes_id > 0:
                        cajas = line.boxes_id * line.product_id.qty_for_box
                        line.product_qty = cajas
                else:
                    if line.boxes_id > 0:
                        cajas = line.boxes_id
                        line.product_qty = cajas
            else:
                line.product_qty = 0