# -*- coding: utf-8 -*-

import json
import time
from ast import literal_eval
from datetime import date, timedelta
from itertools import groupby
from operator import attrgetter, itemgetter
from collections import defaultdict

from odoo import SUPERUSER_ID, _, api, fields, models
from odoo.addons.stock.models.stock_move import PROCUREMENT_PRIORITIES
from odoo.exceptions import UserError
from odoo.osv import expression
from odoo.tools import DEFAULT_SERVER_DATETIME_FORMAT, format_datetime
from odoo.tools.float_utils import float_compare, float_is_zero, float_round
from odoo.tools.misc import format_date

from odoo.exceptions import ValidationError

class StockPicking(models.Model):
    _inherit = "stock.picking"
    
    plate = fields.Many2one('account.analytic.account', string="Placa")
    driver_name = fields.Char(string="Nombre del piloto")
    driver_signature = fields.Many2one('account.analytic.account', string="Firma del piloto")
    driver_signature_id = fields.Char(string="Firma del piloto")
    fuel_total = fields.Float(string="Galones", compute="_sumar_echo")
    despacho_combustible = fields.Boolean(string="Despacho de combustible?", compute='_compute_despacho_combustible')
    medidas_tanque_id = fields.Char(string="Medidas del Tanque")
    medidas_inicial_id = fields.Char(string="Medida inicial")
    medidas_final_id = fields.Char(string="Medida final")
    direccion_entrega_id = fields.Char(string="Dirección de Entrega")
    peso_id = fields.Char(string="Peso")
    medida_id = fields.Char(string="Medida")
    cliente_id = fields.Char(string="Cliente")
    is_refeer = fields.Boolean(string="Refer")
    medida_inicial_refer = fields.Char(string="Medida inicial")
    medida_final_refer = fields.Char(string="Medida final")

    @api.depends('picking_type_id.despacho_combustible')
    def _compute_despacho_combustible(self):
        for picking in self:
            picking.despacho_combustible = picking.picking_type_id.despacho_combustible
    
    @api.depends('move_line_ids_without_package.qty_done')
    def _sumar_echo(self):
        for rec in self:
            rec.fuel_total = sum(line.qty_done for line in rec.move_line_ids_without_package)

    def button_validate(self):
        products_with_insufficient_stock = []

        for rec in self:
            if rec.despacho_combustible:
                for line in rec.move_line_ids_without_package:
                    if line.qty_done == 0.00:
                        raise ValidationError("Las lineas no pueden estar en 0")
                    if line.qty_done > 0.00:
                        quants = self.env['stock.quant'].search([('product_id', '=', line.product_id.id),('location_id', '=', line.location_id.id),])

                    if not any(quant.quantity >= line.qty_done for quant in quants):
                        products_with_insufficient_stock.append(line.product_id.name)

                if products_with_insufficient_stock:
                    products_list = ', '.join(products_with_insufficient_stock)
                    raise ValidationError(f"No hay suficientes existencias para los productos: {products_list}")
        # Clean-up the context key at validation to avoid forcing the creation of immediate
        # transfers.
        ctx = dict(self.env.context)
        ctx.pop('default_immediate_transfer', None)
        self = self.with_context(ctx)

        # Sanity checks.
        pickings_without_moves = self.browse()
        pickings_without_quantities = self.browse()
        pickings_without_lots = self.browse()
        products_without_lots = self.env['product.product']
        for picking in self:
            if not picking.move_lines and not picking.move_line_ids:
                pickings_without_moves |= picking

            picking.message_subscribe([self.env.user.partner_id.id])
            picking_type = picking.picking_type_id
            precision_digits = self.env['decimal.precision'].precision_get('Product Unit of Measure')
            no_quantities_done = all(float_is_zero(move_line.qty_done, precision_digits=precision_digits) for move_line in picking.move_line_ids.filtered(lambda m: m.state not in ('done', 'cancel')))
            no_reserved_quantities = all(float_is_zero(move_line.product_qty, precision_rounding=move_line.product_uom_id.rounding) for move_line in picking.move_line_ids)
            if no_reserved_quantities and no_quantities_done:
                pickings_without_quantities |= picking

            if picking_type.use_create_lots or picking_type.use_existing_lots:
                lines_to_check = picking.move_line_ids
                if not no_quantities_done:
                    lines_to_check = lines_to_check.filtered(lambda line: float_compare(line.qty_done, 0, precision_rounding=line.product_uom_id.rounding))
                for line in lines_to_check:
                    product = line.product_id
                    if product and product.tracking != 'none':
                        if not line.lot_name and not line.lot_id:
                            pickings_without_lots |= picking
                            products_without_lots |= product

        if not self._should_show_transfers():
            if pickings_without_moves:
                raise UserError(_('Please add some items to move.'))
            if pickings_without_quantities:
                raise UserError(self._get_without_quantities_error_message())
            if pickings_without_lots:
                raise UserError(_('You need to supply a Lot/Serial number for products %s.') % ', '.join(products_without_lots.mapped('display_name')))
        else:
            message = ""
            if pickings_without_moves:
                message += _('Transfers %s: Please add some items to move.') % ', '.join(pickings_without_moves.mapped('name'))
            if pickings_without_quantities:
                message += _('\n\nTransfers %s: You cannot validate these transfers if no quantities are reserved nor done. To force these transfers, switch in edit more and encode the done quantities.') % ', '.join(pickings_without_quantities.mapped('name'))
            if pickings_without_lots:
                message += _('\n\nTransfers %s: You need to supply a Lot/Serial number for products %s.') % (', '.join(pickings_without_lots.mapped('name')), ', '.join(products_without_lots.mapped('display_name')))
            if message:
                raise UserError(message.lstrip())

        # Run the pre-validation wizards. Processing a pre-validation wizard should work on the
        # moves and/or the context and never call `_action_done`.
        if not self.env.context.get('button_validate_picking_ids'):
            self = self.with_context(button_validate_picking_ids=self.ids)
        res = self._pre_action_done_hook()
        if res is not True:
            return res

        # Call `_action_done`.
        if self.env.context.get('picking_ids_not_to_backorder'):
            pickings_not_to_backorder = self.browse(self.env.context['picking_ids_not_to_backorder'])
            pickings_to_backorder = self - pickings_not_to_backorder
        else:
            pickings_not_to_backorder = self.env['stock.picking']
            pickings_to_backorder = self
        pickings_not_to_backorder.with_context(cancel_backorder=True)._action_done()
        pickings_to_backorder.with_context(cancel_backorder=False)._action_done()

        if self.user_has_groups('stock.group_reception_report') \
                and self.user_has_groups('stock.group_auto_reception_report') \
                and self.filtered(lambda p: p.picking_type_id.code != 'outgoing'):
            lines = self.move_lines.filtered(lambda m: m.product_id.type == 'product' and m.state != 'cancel' and m.quantity_done and not m.move_dest_ids)
            if lines:
                # don't show reception report if all already assigned/nothing to assign
                wh_location_ids = self.env['stock.location']._search([('id', 'child_of', self.picking_type_id.warehouse_id.view_location_id.ids), ('usage', '!=', 'supplier')])
                if self.env['stock.move'].search([
                        ('state', 'in', ['confirmed', 'partially_available', 'waiting', 'assigned']),
                        ('product_qty', '>', 0),
                        ('location_id', 'in', wh_location_ids),
                        ('move_orig_ids', '=', False),
                        ('picking_id', 'not in', self.ids),
                        ('product_id', 'in', lines.product_id.ids)], limit=1):
                    action = self.action_view_reception_report()
                    action['context'] = {'default_picking_ids': self.ids}
                    return action
        return True

class StockPickingType(models.Model):
    _inherit = "stock.picking.type"
    
    despacho_combustible = fields.Boolean(string="Despacho de combustible")