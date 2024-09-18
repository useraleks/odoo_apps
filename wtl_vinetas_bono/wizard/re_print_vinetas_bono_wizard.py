# -*- coding: utf-8 -*-

from typing import List
from odoo import api, fields, models, _
from odoo.exceptions import UserError, ValidationError
from odoo.addons.base.models.res_partner import _lang_get
import logging

_logger = logging.getLogger(__name__)

class RePrintVinetaBonoWizard(models.TransientModel):
    _name = 're.print.vineta.bono.wizard'
    _description = "Re-Print Vinetas Bono Wizard"

    since = fields.Many2one(comodel_name='vineta.bono', string="Desde")
    until = fields.Many2one(comodel_name='vineta.bono', string="Hasta")
    
    vinetas_to_re_print = fields.One2many(comodel_name='re.print.vineta.bono.wizard.line', inverse_name='re_print_wizard', string=' Viñetas ')
    
    @api.model
    def default_get(self, fields):
        rec = super(RePrintVinetaBonoWizard, self).default_get(fields)
        orders = self._context.get('active_id')
        order_lines = self.env['stock.picking'].browse(orders).label_ids
        exlines = []
        for line in order_lines:
            exlines.append((0, 0, {
                'ro_line_id': line.id,
                'product_id': line.product_id.id,
                'vineta_id': line.vineta_id.id,
                }))
        rec.update({'vinetas_to_re_print': exlines})
        return rec
    
    def apply_booleans(self):
        hasta = self.until.id
        hasta += 1
        lista = (range(self.since.id, hasta))
        orders = self._context.get('active_id')
        rec = self.env['stock.picking'].browse(orders).is_already_printed
        if rec == True:
            raise UserError(
                _('Ya se ha impreso, porfavor solicitar acceso para reimprimir'))
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
    
    def get_labels_to_print(self):
        self.ensure_one()
        labels = []
        for rec in self:
            for line in rec.vinetas_to_re_print:
                if line.selected == True:
                    labels.append(line)
        if not labels:
            raise UserError(
                _('No hay viñetas para reimprimir, porfavor seleccione alguna viñeta para reeimprimir'))
        return labels
    
    def re_print_vineta_bono(self):
        orders = self._context.get('active_id')
        rec = self.env['stock.picking'].browse(orders).is_already_printed
        rec_field = self.env['stock.picking'].browse(orders)
        if rec == True:
            raise UserError(
                _('Ya se ha impreso, porfavor solicitar acceso para reimprimir'))
        else:
            rec_field.is_already_printed = True
            return self.env.ref('wtl_vinetas_bono.action_report_product_label_A4_57x35_re_vineta').report_action(self)
    


class RePrintVinetasBonoWizardLine(models.TransientModel):
    _name = 're.print.vineta.bono.wizard.line'
    _description = "Re-Print Vinetas Bono Wizard Lines"
        
    product_id = fields.Many2one('product.product', string='Producto')
    no_vinetas = fields.Integer(string='No. Viñetas', digits='Cantidad de viñetas a imprimir', default=1.0)
    re_print_wizard = fields.Many2one(comodel_name='re.print.vineta.bono.wizard', string='Wizard')
    date_end = fields.Datetime(string="Fecha Expiracion")
    vineta_id = fields.Many2one(comodel_name='vineta.bono', string="Viñeta")
    selected = fields.Boolean(string='Print', default=False)
    ro_line_id = fields.Many2one('generated.vinetas', string='Lineas de orden')
    barcode = fields.Char(related="vineta_id.barcode")