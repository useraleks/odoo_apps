# -*- coding: utf-8 -*-

from typing import List
from odoo import api, fields, models, _
from odoo.exceptions import UserError, ValidationError
from odoo.addons.base.models.res_partner import _lang_get
import logging

_logger = logging.getLogger(__name__)

class CancelVinetaBonoWizard(models.TransientModel):
    _name = 'cancel.vineta.bono.wizard'
    _description = "Cancel Vinetas Bono Wizard"

    since = fields.Many2one(comodel_name='vineta.bono', string="Desde")
    until = fields.Many2one(comodel_name='vineta.bono', string="Hasta")
    delivery_order = fields.Many2one(comodel_name='stock.picking', string="Orden de entrega")
    
    vinetas_to_cancel = fields.One2many(comodel_name='cancel.vineta.bono.wizard.line', inverse_name='cancel_wizard', string=' Viñetas ')

    def apply_booleans(self):
        hasta = self.until.id
        hasta += 1
        lista = (range(self.since.id, hasta))
        for rec in self:
             if rec.since and rec.until:
                for line in rec.vinetas_to_re_print:
                    if line.vineta_id.id in lista:
                        line.selected = True  
        return {
            "type": "ir.actions.act_window",
            'view_mode': 'form',
            'res_model': 're.print.vineta.bono.wizard',
            'target': 'new',
            'res_id': self.id
        }
    
    def cancel_vineta_bono(self):
        debito = self.env['ir.config_parameter'].sudo().get_param('wtl_vinetas_bono.cuenta_x_pagar')
        credito = self.env['ir.config_parameter'].sudo().get_param('wtl_vinetas_bono.cuenta_gastos')
        for line in self.vinetas_to_cancel:
            if line.selected:
                line.vineta_id.state = "defeated"

        if not debito:
            raise ValidationError(_('No se ha configurado una cuenta de debito para los asientos'))

        if not credito:
            raise ValidationError(_('No se ha configurado una cuenta de credito para los asientos'))

        for rec in self:
            lineas_asiento = []
            ref = "Devolucion de viñetas"

            total_price = sum(line.vineta_id.price for line in rec.vinetas_to_cancel if line.selected)

            if total_price > 0:
                debit_value = {
                    'name': ref,
                    'debit': total_price,
                    'credit': 0.0,
                    'account_id': debito,
                }

                credit_value = {
                    'name': ref,
                    'debit': 0.0,
                    'credit': total_price,
                    'account_id': credito,
                }

                lineas_asiento.append((0, 0, debit_value))
                lineas_asiento.append((0, 0, credit_value))

                vals = {
                    'branch_id': 1,
                    'journal_id': 35,
                    'ref': ref,
                    'line_ids': lineas_asiento,
                }

                asiento_id = self.env['account.move'].create(vals)
                asiento_id.action_post()

    
    @api.model
    def default_get(self, fields):
        rec = super(CancelVinetaBonoWizard, self).default_get(fields)
        orders = self._context.get('active_id')
        order_lines = self.env['stock.picking'].browse(orders).label_ids
        group_id = self.env['stock.picking'].browse(orders).group_id

        delivery_order = self.env['stock.picking'].search([('group_id', '=', group_id.id), ('picking_type_id.code', '=', 'outgoing')], limit=1)

        exlines = []
        for line in delivery_order.label_ids:
            if line.state == "available":
                exlines.append((0, 0, {
                    'ro_line_id': line.id,
                    'product_id': line.product_id.id,
                    'vineta_id': line.vineta_id.id,
                    }))


        rec.update({'delivery_order': delivery_order})
        rec.update({'vinetas_to_cancel': exlines})
        return rec
    
class CancelVinetasBonoWizardLine(models.TransientModel):
    _name = 'cancel.vineta.bono.wizard.line'
    _description = "Cancel Vinetas Bono Wizard Lines"
        
    product_id = fields.Many2one('product.product', string='Producto')
    no_vinetas = fields.Integer(string='No. Viñetas', digits='Cantidad de viñetas a imprimir', default=1.0)
    cancel_wizard = fields.Many2one(comodel_name='cancel.vineta.bono.wizard', string='Wizard')
    date_end = fields.Datetime(string="Fecha Expiracion", related="vineta_id.date_end")
    date_end = fields.Datetime(string="Fecha Expiracion", related="vineta_id.date_end")
    vineta_id = fields.Many2one(comodel_name='vineta.bono', string="Viñeta")
    selected = fields.Boolean(string='Anulacion', default=True)
    ro_line_id = fields.Many2one('generated.vinetas', string='Lineas de orden')
    barcode = fields.Char(related="vineta_id.barcode")
    state = fields.Selection([
        ('available', 'Disponible'),
        ('defeated', 'Anulado'),
        ('paid', 'Pagado'),
    ], string='Estado', index=True, default='available', tracking=True, related="vineta_id.state")
    lot_id = fields.Many2one('stock.lot', string="Lote/Nº de serie", related="vineta_id.lot_id")