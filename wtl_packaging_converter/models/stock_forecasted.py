# -*- coding: utf-8 -*-

from collections import defaultdict
import copy

from odoo import api, models
from odoo.tools import float_compare, float_is_zero, format_date, float_round

class ReplenishmentReport(models.AbstractModel):
    _inherit = "report.stock.report_product_product_replenishment"


    def _get_report_data(self, product_template_ids=False, product_variant_ids=False):
        assert product_template_ids or product_variant_ids
        res = {}

        if self.env.context.get('warehouse') and isinstance(self.env.context['warehouse'], int):
            warehouse = self.env['stock.warehouse'].browse(self.env.context.get('warehouse'))
        else:
            warehouse = self.env['stock.warehouse'].browse(self.get_warehouses()[0]['id'])

        wh_location_ids = [loc['id'] for loc in self.env['stock.location'].search_read(
            [('id', 'child_of', warehouse.view_location_id.id)],
            ['id'],
        )]

        # Get the products we're working, fill the rendering context with some of their attributes.
        if product_template_ids:
            product_templates = self.env['product.template'].browse(product_template_ids)
            res['product_templates'] = product_templates
            res['product_templates_ids'] = product_templates.ids
            res['product_variants'] = product_templates.product_variant_ids
            res['multiple_product'] = len(product_templates.product_variant_ids) > 1
            res['uom'] = product_templates[:1].uom_id.display_name
            res['quantity_on_hand'] = sum(product_templates.mapped('qty_available'))
            res['bx_available'] = sum(product_templates.mapped('bx_available'))
            res['units_available'] = sum(product_templates.mapped('units_available'))
            res['virtual_available'] = sum(product_templates.mapped('virtual_available'))
            res['incoming_qty'] = sum(product_templates.mapped('incoming_qty'))
            res['outgoing_qty'] = sum(product_templates.mapped('outgoing_qty'))
        elif product_variant_ids:
            product_variants = self.env['product.product'].browse(product_variant_ids)
            res['product_templates'] = False
            res['product_variants'] = product_variants
            res['product_variants_ids'] = product_variants.ids
            res['multiple_product'] = len(product_variants) > 1
            res['uom'] = product_variants[:1].uom_id.display_name
            res['quantity_on_hand'] = sum(product_variants.mapped('qty_available'))
            res['bx_available'] = sum(product_variants.mapped('bx_available'))
            res['units_available'] = sum(product_variants.mapped('units_available'))
            res['virtual_available'] = sum(product_variants.mapped('virtual_available'))
            res['incoming_qty'] = sum(product_variants.mapped('incoming_qty'))
            res['outgoing_qty'] = sum(product_variants.mapped('outgoing_qty'))
        res.update(self._compute_draft_quantity_count(product_template_ids, product_variant_ids, wh_location_ids))

        res['lines'] = self._get_report_lines(product_template_ids, product_variant_ids, wh_location_ids)
        return res