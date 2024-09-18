# -*- coding: utf-8 -*-

from odoo import api, fields, models, _
from odoo.exceptions import UserError, ValidationError
import logging

_logger = logging.getLogger(__name__)

class AuthorizeVinetasBonoWizard(models.TransientModel):
    _name = 'authorize.vinetas.bono.wizard'
    _description = "Autorizar Vinetas Bono Wizard"
    
    def get_sale_order(self):
        orders = self._context.get('active_id')
        account_record = self.env['account.move'].browse(orders)
        if account_record:
            return account_record.sale_id

    def get_operation_id(self):
        orders = self._context.get('active_id')
        account_record = self.env['account.move'].browse(orders)
        last_picking = self.env['stock.picking'].search([
                ('group_id', '=', account_record.sale_id.procurement_group_id.id),
                ('is_authorize', '=', False)
            ], order='id desc', limit=1)
        if last_picking:    
            return last_picking

    operation_id = fields.Many2one('stock.picking', string="Entrega", default=get_operation_id)
    sale_id = fields.Many2one('sale.order', string="Venta", default=get_sale_order)

    
    @api.onchange('sale_id')
    def _onchange_sale_id(self):
        if self.sale_id:
            return {'domain': {'operation_id': [('group_id', '=', self.sale_id.procurement_group_id.id), ('is_authorize', '=', False)]}}
        else:
            return {'domain': {'operation_id': []}}


    def authorize_vinetas_bono(self):
        if not self.operation_id:
            raise ValidationError(_('Seleccione una orden de entrega para autorizar las viñetas'))

        self.operation_id.is_authorize = True

        invoice_lines = self.env['account.move.line'].search([
            ('move_id', '=', self._context.get('active_id'))
        ])
        
        for move_line in self.operation_id.move_line_ids_without_package:
            matching_invoice_line = invoice_lines.filtered(lambda line: line.product_id == move_line.product_id)
            if matching_invoice_line:
                move_line.invoiced = sum(matching_invoice_line.mapped('quantity'))