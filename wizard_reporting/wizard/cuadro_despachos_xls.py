# -*- coding: utf-8 -*-

import base64
import io
from odoo import models

class CuadroDespachosXlsx(models.AbstractModel):
    _name = 'report.wizard_reporting.reporte_cuadro_de_despachos_excel'
    _inherit = 'report.report_xlsx.abstract'

    def generate_xlsx_report(self, workbook, data, ordenes):
        sheet = workbook.add_worksheet('ordenes')
        bold = workbook.add_format({'bold': True})

        row = 0
        col = 0

        sheet.write(row, col, 'CLIENTE', bold)
        sheet.write(row, col + 1, 'ESTATUS', bold)
        sheet.write(row, col + 2, 'TAMAÑO/PESO:', bold)
        sheet.write(row, col + 3, 'CONTENEDOR:', bold)
        sheet.write(row, col + 4, 'NAVIERA:', bold)
        sheet.write(row, col + 5, 'PILOTOS:', bold)
        sheet.write(row, col + 6, 'SELECTIVO:', bold)
        sheet.write(row, col + 7, 'DIRECCION:', bold)
        sheet.write(row, col + 8, 'SEGURIDAD:', bold)
        sheet.write(row, col + 9, 'PEAJE:', bold)
        for orden in data['ordenes']:
            row += 1
            sheet.write(row, col, orden['customer_concatenate'])
            sheet.write(row, col + 1, orden['date_status'])
            sheet.write(row, col + 2, orden['x_studio_peso'])
            sheet.write(row, col + 3, orden['contenedor_no_ok'])
            sheet.write(row, col + 4, orden['x_studio_naviera'])
            sheet.write(row, col + 5, orden['pilot_removes_dock'])
            sheet.write(row, col + 6, orden['x_studio_selectivo'])
            sheet.write(row, col + 7, orden['x_studio_direccin_de_entrega'])
            sheet.write(row, col + 8, orden['x_studio_seguridad'])
            sheet.write(row, col + 9, orden['x_studio_peaje'])
