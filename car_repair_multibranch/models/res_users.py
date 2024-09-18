# -*- coding: utf-8 -*-

from odoo import api, fields, models, _

class ResUsers(models.Model):
    _inherit = 'res.users'
    
    comp_rama = fields.Many2one('res.company', string="Compañia")
    santotomascar = fields.Boolean(string="santotomas")
    puertoquetzalcar = fields.Boolean('Puerto Quetzal', default=False)