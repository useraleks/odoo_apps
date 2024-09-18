# -*- coding: utf-8 -*-

from odoo import fields, models, api, _

class SaleReport(models.Model):
    _inherit = "sale.report"

    bx_available_idd = fields.Integer(string="Cajas")
    units_available_idd = fields.Integer(string="Unidades")

    '''@api.depends('product_uom_qty', 'product_tmpl_id.qty_for_box')
    def _get_box_available(self):
        for line in self:
            if line.product_tmpl_id.qty_for_box > 0 and line.product_uom_qty > 0:
                if line.product_uom.is_unit:
                    total = line.product_uom_qty / line.product_tmpl_id.qty_for_box
                    caja_completa = int(total)
                    line.bx_available = caja_completa
                else:
                    total = line.product_uom_qty
                    caja_completa = int(total)
                    line.bx_available = caja_completa
            else:
                line.bx_available = 0

    @api.depends('product_uom_qty', 'product_tmpl_id.qty_for_box')
    def _get_units_available(self):
        for line in self:
            if line.product_tmpl_id.qty_for_box > 0 and line.product_uom_qty > 0:
                if line.product_uom.is_unit:
                    total = line.product_uom_qty / line.product_tmpl_id.qty_for_box
                    caja_completa = int(total)
                    unidades_sin_redondeo = total - caja_completa
                    unidades_redondeadas = round(unidades_sin_redondeo, 2)
                    unidades_sueltas = int(round(unidades_redondeadas * line.product_tmpl_id.qty_for_box))
                    line.units_available = unidades_sueltas
                else:
                    total = line.product_uom_qty
                    caja_completa = int(total)
                    unidades_sin_redondeo = total - caja_completa
                    unidades_redondeadas = round(unidades_sin_redondeo, 2)
                    unidades_sueltas = int(round(unidades_redondeadas * line.product_tmpl_id.qty_for_box))
                    line.units_available = unidades_sueltas
            else:
                line.units_available = 0'''