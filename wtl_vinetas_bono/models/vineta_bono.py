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

class VinetaBono (models.Model):
    _name = 'vineta.bono'
    _description = 'Vinetas Bono'
    _inherit = ["mail.thread", "mail.activity.mixin"]

    name = fields.Char(string='Referencia', required=True, copy=False, readonly=True, default=lambda self: _('New'))
    product_id = fields.Many2one('product.product' ,string="Producto")
    partner_id = fields.Many2one('res.partner' ,string="Cliente")
    date_begin = fields.Datetime(string="Fecha de inicio", default=fields.Datetime.now)
    date_end = fields.Datetime(string="Fecha Expiracion")
    generated_by = fields.Many2one('res.users', string='Generada por', default=lambda self: self.env.user)
    state = fields.Selection([
        ('available', 'Disponible'),
        ('defeated', 'Anulado'),
        ('paid', 'Pagado'),
    ], string='Estado', index=True, default='available', tracking=True)
    barcode = fields.Char(string="Codigo de barras", required=True, copy=False, readonly=True, default=lambda self: _('New'))
    note = fields.Html(string="nota")
    origin_id = fields.Many2one('sale.order', string="Origen")
    manufacturer_id = fields.Many2one('medicine.manufacturer', string="Laboratorio", related="product_id.manufacturer_id")
    qr_code = fields.Binary(string="Código QR", attachment=True, store=True)
    price = fields.Float(string="Precio de Viñeta")
    invoice_ids = fields.Many2many('account.move', string="Facturas", related="origin_id.invoice_ids")
    lot_id = fields.Many2one('stock.lot', string="Lote/Nº de serie")
    payment_date = fields.Datetime(string="Fecha de pago")
    sales_person = fields.Many2one('res.users', related="origin_id.user_id", string="Vendedor")
    delivery_order = fields.Many2one('stock.picking', string="Orden de entrega")
    searchable_name = fields.Char(compute='_compute_searchable_name', store=True)

    @api.onchange('product_id', 'product_id.manufacturer_id')
    def onchange_product_id(self):
        self.manufacturer_id = self.product_id.manufacturer_id.id

    @api.depends('name')
    def _compute_searchable_name(self):
        for vineta in self:
            if vineta.name:
                vineta.searchable_name = vineta.name
            else:
                pass

    @api.model
    def name_search(self, name='', args=None, operator='ilike', limit=100):
        if not args:
            args = []

        domain = ['|', ('name', operator, name), ('barcode', operator, name)]
        records = self.search(domain + args, limit=limit)
        return records.name_get()


    @api.model
    def create(self, vals):
        if vals.get('name', _('New')) == _('New'):
            vals['name'] = self.env['ir.sequence'].next_by_code('vineta.bono.barcode') or _('New')
            barcode_sequence = self.env['ir.sequence'].next_by_code('vineta.bono.barcode') or _('New')
            vals['name'] = self._convert_to_hex(barcode_sequence)

        result = super(VinetaBono, self).create(vals)
        return result

    def _convert_to_hex(self, sequence):
        return format(int(sequence), 'X').zfill(6)
    
    def action_mark_as_paid(self):
        self.state = 'paid'
        self.payment_date = Datetime.now()

    def action_mark_as_defeated(self):
        # Inicializamos total_price, ref y lineas_asiento fuera del bucle
        total_price = 0
        ref = "Anulacion de viñetas: "
        lineas_asiento = []
        viñetas_anuladas = []
        debito = self.env['ir.config_parameter'].sudo().get_param('wtl_vinetas_bono.cuenta_x_pagar')
        credito = self.env['ir.config_parameter'].sudo().get_param('wtl_vinetas_bono.cuenta_gastos')

        for rec in self:
            if rec.state == 'paid':
                raise ValidationError(_(
                    'Solo puedes anular viñetas en estado DISPONIBLE'
                ))
            elif rec.state == 'defeated':
                raise ValidationError(_(
                    'La viñeta {} ya está anulada.'.format(rec.name)
                ))
            else:
                rec.state = 'defeated'
                total_price += rec.price
                viñetas_anuladas.append(rec.name)
        
        if not debito:
            raise ValidationError(_('No se ha configurado una cuenta de debito para los asientos'))

        if not credito:
            raise ValidationError(_('No se ha configurado una cuenta de credito para los asientos'))

        if total_price > 0:
            ref += ', '.join(viñetas_anuladas)

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


    
    def get_qr(self):
        for invoice in self:
            id = invoice.id

            url = f'https://solyruiz-jomi-copy-v02-stg-12565572.dev.odoo.com/web#id=41&menu_id=710&cids=1&action=1055&model=vineta.bono&view_type=form'
            

            response = requests.get(url)

            qr = qrcode.QRCode(
                version=1,
                error_correction=qrcode.constants.ERROR_CORRECT_L,
                box_size=2.7,
                border=0
            )
            qr.add_data(url)
            qr.make(fit=True)
            img = qr.make_image(fill_color="black", back_color="white")

            img_pil = img.get_image()

            img_pil = img_pil.resize((15, 15), Image.ANTIALIAS)

            output = io.BytesIO()
            img.save(output, format="PNG")
            invoice.qr_code = base64.b64encode(output.getvalue())

            output.close()