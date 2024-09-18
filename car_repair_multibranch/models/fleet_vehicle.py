# -*- coding: utf-8 -*-

from odoo import models, fields, api

class FleetVehicle(models.Model):
    _inherit = 'fleet.vehicle'

    company_branch = fields.Many2one("res.company", string="Compañia Taller")