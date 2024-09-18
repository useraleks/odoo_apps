# -*- coding: utf-8 -*-

from odoo import fields, models, api, _

class StockLot(models.Model):
    _inherit = "stock.lot"

    qty_box_available = fields.Char(string="Disponible", compute="get_box_units")
    bx_available = fields.Float(string="Cajas", compute="get_box_available")
    units_available = fields.Float(string="Unidades", compute="get_units_available")

    @api.depends('product_qty', 'product_id.qty_for_box')
    def get_box_available(self):
        for line in self:
            if line.product_id.qty_for_box > 0 and line.product_qty > 0:
                if line.product_uom_id.is_unit:
                    total = line.product_qty / line.product_id.qty_for_box
                    caja_completa = int(total)
                    line.bx_available = caja_completa
                else:
                    total = line.product_qty
                    caja_completa = int(total)
                    line.bx_available = caja_completa
            else:
                line.bx_available = 0

    @api.depends('product_qty', 'product_id.qty_for_box')
    def get_units_available(self):
        for line in self:
            if line.product_id.qty_for_box > 0 and line.product_qty > 0:
                if line.product_id.uom_id.is_unit:
                    total = line.product_qty / line.product_id.qty_for_box
                    caja_completa = int(total)
                    unidades_sin_redondeo = total - caja_completa
                    unidades_redondeadas = round(unidades_sin_redondeo, 2)
                    unidades_sueltas = int(round(unidades_redondeadas * line.product_id.qty_for_box))
                    line.units_available = unidades_sueltas
                else:
                    total = line.product_qty
                    caja_completa = int(total)
                    unidades_sin_redondeo = total - caja_completa
                    unidades_redondeadas = round(unidades_sin_redondeo, 2)
                    unidades_sueltas = int(round(unidades_redondeadas * line.product_id.qty_for_box))
                    line.units_available = unidades_sueltas
            else:
                line.units_available = 0

    @api.depends('units_available', 'bx_available')
    def get_box_units(self):
        for line in self:
            line.qty_box_available = f"{line.bx_available} Cajas y {line.units_available} Unidades"