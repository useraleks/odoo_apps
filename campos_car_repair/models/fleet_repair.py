# -*- coding: utf-8 -*-

from odoo import api, fields, models, _

class HrExpense(models.Model):
    _inherit = 'fleet.repair'
    
    employee_id = fields.Many2one('res.users', string='Supervisor', default=lambda self: self.env.user, required=True, readonly=True)