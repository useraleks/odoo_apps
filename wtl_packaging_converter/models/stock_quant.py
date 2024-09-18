# -*- coding: utf-8 -*-

from odoo import fields, models, api, _

class StockQuant(models.Model):
    _inherit = "stock.quant"

    bx_available = fields.Integer(string="Cajas", compute="_get_box_available")
    units_available = fields.Integer(string="Unidades", compute="_get_units_available")

    @api.depends('quantity', 'product_id.qty_for_box', 'product_uom_id')
    def _get_box_available(self):
        for line in self:
            if line.product_id.qty_for_box > 0 and line.quantity > 0:
                if line.product_uom_id.is_unit:
                    total = line.quantity / line.product_id.qty_for_box
                    caja_completa = int(total)
                    line.bx_available = caja_completa
                else:
                    total = line.quantity
                    caja_completa = int(total)
                    line.bx_available = caja_completa
            else:
                line.bx_available = 0

    @api.depends('quantity', 'product_id.qty_for_box')
    def _get_units_available(self):
        for line in self:
            if line.product_id.qty_for_box > 0 and line.quantity > 0:
                if line.product_id.uom_id.is_unit:
                    total = line.quantity / line.product_id.qty_for_box
                    caja_completa = int(total)
                    unidades_sin_redondeo = total - caja_completa
                    unidades_redondeadas = round(unidades_sin_redondeo, 2)
                    unidades_sueltas = int(round(unidades_redondeadas * line.product_id.qty_for_box))
                    line.units_available = unidades_sueltas
                else:
                    total = line.quantity
                    caja_completa = int(total)
                    unidades_sin_redondeo = total - caja_completa
                    unidades_redondeadas = round(unidades_sin_redondeo, 2)
                    unidades_sueltas = int(round(unidades_redondeadas * line.product_id.qty_for_box))
                    line.units_available = unidades_sueltas
            else:
                line.units_available = 0