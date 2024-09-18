# -*- coding: utf-8 -*-

from odoo import api, fields, models, _

class ResUsers(models.Model):
    _inherit = 'res.users'
    
    santotomas = fields.Boolean(string="Es Santotomas")
    puertoquetzal = fields.Boolean(string="Es PuertoQuetzal")