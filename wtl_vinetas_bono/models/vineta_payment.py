# -*- coding: utf-8 -*

from odoo import api, fields, models, _
import num2words as n2w
import requests
import base64
import qrcode
from PIL import Image
import io
from odoo.exceptions import UserError, ValidationError, Warning
import datetime
from odoo.fields import Datetime

class VinetaPayment(models.Model):
    _name = 'vineta.payment'
    _description = 'Vinetas Payment'
    _inherit = ["mail.thread", "mail.activity.mixin"]

    name = fields.Char(string='Referencia', required=True, copy=False, readonly=True, default=lambda self: _('New'))
    payment_date = fields.Datetime(string="Fecha de pago", default=fields.Datetime.now)
    payment_line = fields.One2many('vineta.payment.line', 'vineta_payment', string='Viñetas')
    partner_id = fields.Many2one('res.partner', string="Cliente")
    state = fields.Selection([
        ('draft', 'Borrador'),
        ('done', 'Confirmado'),
    ], string='Estado', index=True, default='draft', tracking=True)
    salesperson = fields.Many2one('res.users', string="Vendedor (a)")
    amount_total = fields.Float(compute='_amount_all',string='Total', store=True, readonly=True, tracking=True)

    @api.model
    def create(self, vals):
        if vals.get('name', _('New')) == _('New'):
            vals['name'] = self.env['ir.sequence'].next_by_code('vineta.bono') or _('New')

        result = super(VinetaPayment, self).create(vals)
        return result
    
    def action_mark_as_paid(self):
        for rec in self:
            defeated_lines = []
            paid_lines = []
            
            for line in rec.payment_line:
                if line.vineta_id.state == 'defeated':
                    defeated_lines.append(line.vineta_id.name)
                if line.vineta_id.state == 'paid':
                    paid_lines.append(line.vineta_id.name)
            
            if defeated_lines:
                raise ValidationError(_(
                    f'Las siguientes viñetas están ya anuladas: {", ".join(defeated_lines)}'
                ))
            
            if paid_lines:
                raise ValidationError(_(
                    f'Las siguientes viñetas están ya pagadas: {", ".join(paid_lines)}'
                ))
            
            for line in rec.payment_line:
                line.vineta_id.state = "paid"
                line.vineta_id.payment_date = rec.payment_date
            
            rec.state = 'done'


    def action_set_draft(self):
        for rec in self:
            for line in rec.payment_line:
                line.vineta_id.state = "available"
            rec.state = 'draft'
            
    @api.depends('payment_line.price')
    def _amount_all(self):
        for order in self:
            total_price = 0.0
            for line in order.payment_line:
                total_price += line.price
            order.update({
                'amount_total': total_price,})
    
class VinetaPaymentLine(models.TransientModel):
    _name = 'vineta.payment.line'
    _description = "Lines of payment"
    
    vineta_id = fields.Many2one('vineta.bono', string="Viñeta")
    product_id = fields.Many2one('product.product', string='Producto', related="vineta_id.product_id")
    vineta_payment = fields.Many2one('vineta.payment', string='Vineta Payment')
    state = fields.Selection([
        ('available', 'Disponible'),
        ('defeated', 'Anulado'),
        ('paid', 'Pagado'),
    ], string='Estado', index=True, related="vineta_id.state")
    price = fields.Float(string="Precio de Viñeta", related="vineta_id.price")
    lot_id = fields.Many2one('stock.lot', string="Lote/Nº de serie", related="vineta_id.lot_id")
    invoice_ids = fields.Many2many('account.move', string="Facturas", related="vineta_id.invoice_ids")
    salesperson = fields.Many2one('res.users', string="Comercial", related="vineta_id.generated_by")
    partner_id = fields.Many2one('res.partner' ,string="Cliente", related="vineta_id.partner_id")

    @api.constrains('vineta_id', 'vineta_payment')
    def _check_unique_vineta(self):
        for line in self:
            duplicate_lines = self.search([
                ('vineta_id', '=', line.vineta_id.id),
                ('vineta_payment', '=', line.vineta_payment.id),
                ('id', '!=', line.id)
            ])

            defeated_lines = []
            if duplicate_lines:
                duplicate_names = ', '.join(duplicate_lines.mapped('vineta_id.name'))
                raise ValidationError(_(
                    'Las siguientes viñetas están duplicadas en las líneas de pago: %s' % duplicate_names
                ))