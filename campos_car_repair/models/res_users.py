# -*- coding: utf-8 -*-

from odoo import api, fields, models, _

class ResUsers(models.Model):
    _inherit = 'res.users'
    
    company_rama = fields.Many2one('res.company', string="Compañia")