# -*- coding: utf-8 -*-

from odoo import fields, models, api, _

class StockMoveLine(models.Model):
    _inherit = "stock.move.line"

    bx_available = fields.Integer(string="Cajas", compute="_get_box_available")
    units_available = fields.Integer(string="Unidades", compute="_get_units_available")

    @api.depends('qty_done', 'product_id.qty_for_box')
    def _get_box_available(self):
        for line in self:
            if line.product_id.qty_for_box > 0 and line.qty_done > 0:
                if line.product_uom_id.is_unit:
                    total = line.qty_done / line.product_id.qty_for_box
                    caja_completa = int(total)
                    line.bx_available = caja_completa
                else:
                    total = line.qty_done
                    caja_completa = int(total)
                    line.bx_available = caja_completa
            else:
                line.bx_available = 0

    @api.depends('qty_done', 'product_id.qty_for_box')
    def _get_units_available(self):
        for line in self:
            if line.product_id.qty_for_box > 0 and line.qty_done > 0:
                if line.product_id.uom_id.is_unit:
                    total = line.qty_done / line.product_id.qty_for_box
                    caja_completa = int(total)
                    unidades_sin_redondeo = total - caja_completa
                    unidades_redondeadas = round(unidades_sin_redondeo, 2)
                    unidades_sueltas = int(round(unidades_redondeadas * line.product_id.qty_for_box))
                    line.units_available = unidades_sueltas
                else:
                    total = line.qty_done
                    caja_completa = int(total)
                    unidades_sin_redondeo = total - caja_completa
                    unidades_redondeadas = round(unidades_sin_redondeo, 2)
                    unidades_sueltas = int(round(unidades_redondeadas * line.product_id.qty_for_box))
                    line.units_available = unidades_sueltas
            else:
                line.units_available = 0

class StockMove(models.Model):
    _inherit = "stock.move"

    bx_available = fields.Integer(string="Cajas", compute="_get_box_available")
    units_available = fields.Integer(string="Unidades", compute="_get_units_available")

    @api.depends('product_uom_qty', 'product_id.qty_for_box')
    def _get_box_available(self):
        for line in self:
            if line.product_id.qty_for_box > 0 and line.product_uom_qty > 0:
                if line.product_uom.is_unit:
                    total = line.product_uom_qty / line.product_id.qty_for_box
                    caja_completa = int(total)
                    line.bx_available = caja_completa
                else:
                    total = line.product_uom_qty
                    caja_completa = int(total)
                    line.bx_available = caja_completa
            else:
                line.bx_available = 0

    @api.depends('product_uom_qty', 'product_id.qty_for_box')
    def _get_units_available(self):
        for line in self:
            if line.product_id.qty_for_box > 0 and line.product_uom_qty > 0:
                if line.product_uom.is_unit:
                    total = line.product_uom_qty / line.product_id.qty_for_box
                    caja_completa = int(total)
                    unidades_sin_redondeo = total - caja_completa
                    unidades_redondeadas = round(unidades_sin_redondeo, 2)
                    unidades_sueltas = int(round(unidades_redondeadas * line.product_id.qty_for_box))
                    line.units_available = unidades_sueltas
                else:
                    total = line.product_uom_qty
                    caja_completa = int(total)
                    unidades_sin_redondeo = total - caja_completa
                    unidades_redondeadas = round(unidades_sin_redondeo, 2)
                    unidades_sueltas = int(round(unidades_redondeadas * line.product_id.qty_for_box))
                    line.units_available = unidades_sueltas
            else:
                line.units_available = 0