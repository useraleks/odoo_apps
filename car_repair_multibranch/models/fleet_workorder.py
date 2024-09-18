# -*- coding: utf-8 -*-

from odoo import models, fields, api

class FleetWorkOrder(models.Model):
    _inherit = 'fleet.workorder'

    mechanic_id = fields.Many2one('hr.employee', string="Mecanico", related="diagnose_id.mechanic_id")