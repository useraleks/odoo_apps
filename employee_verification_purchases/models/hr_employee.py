# -*- coding: utf-8 -*-

from odoo import models, fields, api

class HrEmployee(models.Model):
    _inherit = 'hr.employee'

    ispurchase = fields.Boolean(string="¿Area de compras?")
    codeemployee = fields.Char(string="Codigo")