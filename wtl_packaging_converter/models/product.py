# -*- coding: utf-8 -*-

from odoo import api, fields, models, _
from odoo.exceptions import UserError
from itertools import groupby
from operator import itemgetter
from datetime import date

class ProductTemplate(models.Model):
    _inherit = "product.template"

    qty_for_box = fields.Float(string="Cantidad por caja")
    qty_for_blister = fields.Float(string="Cantidad por Blister")
    qty_box_available = fields.Char(string="Disponible", compute="get_box_units")
    bx_available = fields.Integer(string="Cajas", compute="_get_box_available")
    units_available = fields.Integer(string="Unidades", compute="_get_units_available")

    @api.depends('qty_available', 'qty_for_box')
    def _get_box_available(self):
        for line in self:
            if line.qty_for_box > 0 and line.qty_available > 0:
                if line.uom_id.is_unit:
                    total = line.qty_available / line.qty_for_box
                    caja_completa = int(total)
                    line.bx_available = caja_completa
                else:
                    total = line.qty_available
                    caja_completa = int(total)
                    line.bx_available = caja_completa
            else:
                line.bx_available = 0

    @api.depends('qty_available', 'qty_for_box')
    def _get_units_available(self):
        for line in self:
            if line.qty_for_box > 0 and line.qty_available > 0:
                if line.uom_id.is_unit:
                    total = line.qty_available / line.qty_for_box
                    caja_completa = int(total)
                    unidades_sin_redondeo = total - caja_completa
                    unidades_redondeadas = round(unidades_sin_redondeo, 2)
                    unidades_sueltas = int(round(unidades_redondeadas * line.qty_for_box))
                    line.units_available = unidades_sueltas
                else:
                    total = line.qty_available
                    caja_completa = int(total)
                    unidades_sin_redondeo = total - caja_completa
                    unidades_redondeadas = round(unidades_sin_redondeo, 2)
                    unidades_sueltas = int(round(unidades_redondeadas * line.qty_for_box))
                    line.units_available = unidades_sueltas
            else:
                line.units_available = 0

    @api.depends('units_available', 'bx_available')
    def get_box_units(self):
        for line in self:
            line.qty_box_available = f"{line.bx_available} Cajas y {line.units_available} Unidades"

    def show_qty_boxes(self):
        pass

class ProductProduct(models.Model):
    _inherit = "product.product"

    """qty_for_box = fields.Float(string="Cantidad por caja")
    qty_for_blister = fields.Float(string="Cantidad por Blister")
    qty_box_available = fields.Float(string="Caja", compute="_onchange_qty_available")"""

    def show_qty_boxes(self):
        pass

    def get_product_info_pos(self, price, quantity, pos_config_id):
        self.ensure_one()
        config = self.env['pos.config'].browse(pos_config_id)
        
        # Tax related
        taxes = self.taxes_id.compute_all(price, config.currency_id, quantity, self)
        grouped_taxes = {}
        for tax in taxes['taxes']:
            if tax['id'] in grouped_taxes:
                grouped_taxes[tax['id']]['amount'] += tax['amount']/quantity if quantity else 0
            else:
                grouped_taxes[tax['id']] = {
                    'name': tax['name'],
                    'amount': tax['amount']/quantity if quantity else 0
                }

        all_prices = {
            'price_without_tax': taxes['total_excluded']/quantity if quantity else 0,
            'price_with_tax': taxes['total_included']/quantity if quantity else 0,
            'tax_details': list(grouped_taxes.values()),
        }

        # Pricelists
        if config.use_pricelist:
            pricelists = config.available_pricelist_ids
        else:
            pricelists = config.pricelist_id
        price_per_pricelist_id = pricelists._price_get(self, quantity)
        pricelist_list = [{'name': pl.name, 'price': price_per_pricelist_id[pl.id]} for pl in pricelists]

        # Warehouses
        warehouse_list = []
        for w in self.env['stock.warehouse'].search([]):
            available_quantity = self.with_context({'warehouse': w.id}).qty_available
            forecasted_quantity = self.with_context({'warehouse': w.id}).virtual_available

            qty_for_caja = self.qty_for_box

            if qty_for_caja > 0:
                if self.uom_id.is_unit:
                    available_boxes = available_quantity / qty_for_caja
                    available_boxes_redondeado = int(available_boxes)
                    available_units = int(round((available_boxes - available_boxes_redondeado), 2) * qty_for_caja)
                    forecasted_boxes = int(forecasted_quantity // qty_for_caja)
                    forecasted_units = round((forecasted_quantity % qty_for_caja), 2) * qty_for_caja

                    uom_boxes_available = f"{available_boxes_redondeado} Cajas Y {available_units} Unidades"
                    uom_boxes_forecasted = f"{forecasted_boxes} Cajas y {forecasted_units} unidades"
                else:
                    available_boxes = available_quantity
                    available_boxes_redondeado = int(available_boxes)
                    available_units = int(round((available_boxes - available_boxes_redondeado), 2) * qty_for_caja)
                    forecasted_boxes = int(forecasted_quantity // qty_for_caja)
                    forecasted_units = round((forecasted_quantity % qty_for_caja), 2) * qty_for_caja

                    uom_boxes_available = f"{available_boxes_redondeado} Cajas Y {available_units} Unidades"
                    uom_boxes_forecasted = f"{forecasted_boxes} Cajas y {forecasted_units} unidades"
            else:
                uom_boxes_available = f"Cantidad por Caja?"
                uom_boxes_forecasted = f"{0} Cajas y {0} unidades"

            warehouse_list.append({
                'name': w.name,
                'available_quantity': available_quantity,
                'forecasted_quantity': forecasted_quantity,
                'uom': self.uom_name,
                'uom_boxes_available': uom_boxes_available,
                'uom_boxes_forecasted': uom_boxes_forecasted,
            })

        # Suppliers
        key = itemgetter('partner_id')
        supplier_list = []
        for key, group in groupby(sorted(self.seller_ids, key=key), key=key):
            for s in list(group):
                if not((s.date_start and s.date_start > date.today()) or (s.date_end and s.date_end < date.today()) or (s.min_qty > quantity)):
                    supplier_list.append({
                        'name': s.partner_id.name,
                        'delay': s.delay,
                        'price': s.price
                    })
                    break

        # Variants
        variant_list = [{'name': attribute_line.attribute_id.name,
                        'values': list(map(lambda attr_name: {'name': attr_name, 'search': '%s %s' % (self.name, attr_name)}, attribute_line.value_ids.mapped('name')))}
                        for attribute_line in self.attribute_line_ids]

        return {
            'all_prices': all_prices,
            'pricelists': pricelist_list,
            'warehouses': warehouse_list,
            'suppliers': supplier_list,
            'variants': variant_list
        }
