# -*- coding: utf-8 -*-

from odoo import models, fields, api

class ResCompany(models.Model):
    _inherit = 'res.company'

    puertoquetzal = fields.Boolean(string="Puerto Quetzal")
    santotomas = fields.Boolean(string="Santo Tomas")