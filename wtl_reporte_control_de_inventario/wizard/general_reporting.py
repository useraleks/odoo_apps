# -*- coding: utf-8 -*-

from odoo import models, fields, api
from odoo.exceptions import ValidationError
from datetime import datetime
import pytz

class WizGeneralReporting(models.TransientModel):
    _name = 'wiz.general.reporting'
    _description = 'Wizard General Reporting'

    type_of_report = fields.Selection([('controldeinventario','Control De Inventario')], 'Tipo de Reporte')
    initial_date = fields.Datetime(string="Fecha Inicial")
    end_date = fields.Datetime(string="Fecha Final")
    product_id = fields.Many2one('product.product', string="Producto")

    def translate_weekday(self, weekday):
        translation_mapping = {
            'Monday': 'Lunes',
            'Tuesday': 'Martes',
            'Wednesday': 'Miércoles',
            'Thursday': 'Jueves',
            'Friday': 'Viernes',
            'Saturday': 'Sábado',
            'Sunday': 'Domingo',
        }
        return translation_mapping.get(weekday, weekday)

    def format_date(self, datetime_str):
        if datetime_str:
            datetime_obj = fields.Datetime.from_string(datetime_str)
            formatted_date = datetime_obj.strftime('%d-%m-%Y %I%p %A')
            formatted_date = ' '.join(self.translate_weekday(part) for part in formatted_date.split())
            return formatted_date
        return ''


    def calculate_initial_units(self):
        for rec in self:
            producto = rec.product_id
            quants = self.env['product.product'].search([
                    ('product_id', '=', producto.id),
                ])

    def print_reporting(self):
        for record in self:
            #if record.type_of_report == 'cuadrodespachos':

                domain = []
                if record.initial_date:
                    domain += [('create_date', '>=', record.initial_date)]
                if record.end_date:
                    domain += [('create_date', '<=', record.end_date)]
                if record.product_id:
                    domain += [('product_id', '=', record.product_id.id)]
                registros = self.env['stock.valuation.layer'].search_read(domain, order='create_date')

                if record.product_id:
                    qty_product = record.product_id.qty_available

                    producto_costo = record.product_id.standard_price
                    
                    for rec in registros:
                        if 'quantity' in rec and rec['quantity'] >= 1:
                            qty_product -= rec['quantity']
                        else:
                            pass
                

                    for rek in registros:
                        if 'quantity' in rek and rek['quantity'] <= 0:
                            valor = rek['quantity']
                            valor_positivo = abs(valor)
                            qty_product += valor_positivo
                        else:
                            pass
                else:
                    raise ValidationError('Porfavor seleccione el producto')
                
                for registro in registros:
                    if registro.get('create_date'):
                        create_date_str = registro['create_date'].strftime('%d/%m/%Y')
                        registro['create_date'] = create_date_str

                guatemala_tz = pytz.timezone('America/Guatemala')
                now = datetime.now()
                current_time = now.replace(tzinfo=pytz.utc).astimezone(guatemala_tz)
                formatted_time = current_time.strftime("%d/%m/%Y %H:%M:%S %p")


                data = {
                    'form_data': self.read()[0],
                    'registros' : registros,
                    'product_name': record.product_id.name,
                    'product_code': record.product_id.default_code,
                    'desde': record.initial_date.strftime('%d/%m/%Y'),
                    'hasta': record.end_date.strftime('%d/%m/%Y'),
                    'qty_product': qty_product,
                    'producto_costo': producto_costo,
                    'formatted_time': formatted_time,
                }
        return self.env.ref("wtl_reporte_control_de_inventario.action_control_de_inventario").report_action(self, data=data)

    def print_reporting_excel(self):
        for record in self:
            if record.type_of_report == 'cuadrodespachos':
                domain = []
                if record.initial_date:
                    domain += [('x_studio_fecha_de_salida', '>=', record.initial_date)]
                if record.end_date:
                    domain += [('x_studio_fecha_de_salida', '<=', record.end_date)]
                registros = self.env['sale.order'].search_read(domain, order='x_studio_fecha_de_salida, partner_id')

                data = {
                    'form_data': self.read()[0],
                    'registros' : registros
                }
                return self.env.ref("wizard_reporting.action_cuadro_de_despachos_excel").report_action(self, data=data)