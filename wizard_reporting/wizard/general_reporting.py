# -*- coding: utf-8 -*-

from odoo import models, fields, api
from odoo.exceptions import ValidationError

class WizGeneralReporting(models.TransientModel):
    _name = 'wiz.general.reporting'
    _description = 'Wizard General Reporting'

    type_of_report = fields.Selection([('cuadrodespachos','Cuadros De Despachos')], 'Tipo de Reporte')
    initial_date = fields.Datetime(string="Fecha Inicial")
    end_date = fields.Datetime(string="Fecha Final")

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

    def print_reporting(self):
        for record in self:
            if record.type_of_report == 'cuadrodespachos':
                domain = []
                if record.initial_date:
                    domain += [('x_studio_fecha_de_salida', '>=', record.initial_date)]
                if record.end_date:
                    domain += [('x_studio_fecha_de_salida', '<=', record.end_date)]
                ordenes = self.env['sale.order'].search_read(domain, order='x_studio_fecha_de_salida, partner_id')

                data = {
                    'form_data': self.read()[0],
                    'ordenes' : ordenes
                }
                return self.env.ref("wizard_reporting.action_cuadro_de_despachos").report_action(self, data=data)

    def print_reporting_excel(self):
        for record in self:
            if record.type_of_report == 'cuadrodespachos':
                domain = []
                if record.initial_date:
                    domain += [('x_studio_fecha_de_salida', '>=', record.initial_date)]
                if record.end_date:
                    domain += [('x_studio_fecha_de_salida', '<=', record.end_date)]
                ordenes = self.env['sale.order'].search_read(domain, order='x_studio_fecha_de_salida, partner_id')

                data = {
                    'form_data': self.read()[0],
                    'ordenes' : ordenes
                }
                return self.env.ref("wizard_reporting.action_cuadro_de_despachos_excel").report_action(self, data=data)