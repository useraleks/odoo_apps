# -*- coding: utf-8 -*-

from odoo import models, fields, api

class HrEmployee(models.Model):
    _inherit = 'hr.employee'

    is_car_repair = fields.Boolean(string="¿Area de taller?")
    is_supervisor = fields.Boolean(string="Supervisor")
    supervisor_code = fields.Char(string="Codigo")
    is_driver = fields.Boolean(string="Piloto")
    is_mechanic = fields.Boolean(string="Mecanico")
    company_branch = fields.Many2one("res.company", string="Compañia")