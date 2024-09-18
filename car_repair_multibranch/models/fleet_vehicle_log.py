# -*- coding: utf-8 -*-

from odoo import models, fields, api

class FleetWorkOrder(models.Model):
    _inherit = 'fleet.vehicle.log.services'

    piloto_id = fields.Many2one('hr.employee', string='Piloto')
    id_reparacion = fields.Many2one('fleet.repair', string="ID de la reparacion")
    