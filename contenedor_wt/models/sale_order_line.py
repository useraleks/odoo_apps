# -*- coding: utf-8 -*-

from odoo import models, fields, api

class rlmSalesOrder(models.Model):
    _inherit = 'sale.order.line'

    contenedor_no = fields.Char(string="Contenedor No.", related='order_id.contenedor_no_ok')