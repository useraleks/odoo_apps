# -*- coding: utf-8 -*-

from odoo import models, fields, api

from odoo.exceptions import AccessError, UserError, ValidationError

class PurchaseOrder(models.Model):
    _inherit = 'purchase.order'

    employee_id = fields.Many2one('hr.employee', string='Empleado', domain=[('ispurchase', '=', True)], required=True)
    codigo_ok = fields.Char(string='Codigo', required=True)