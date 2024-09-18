# -*- coding: utf-8 -*-

from odoo import models, fields, api

class FleetVehicleOdometer(models.Model):
    _inherit = 'fleet.vehicle.odometer'

    driver = fields.Many2one('hr.employee', string="Piloto")
    ref_reception = fields.Many2one('reception.vehicle', string="Ref en recepcion")
    ref_taller = fields.Many2one('reception.vehicle', string="Ref en Taller")
    fecha = fields.Datetime(string='Fecha', default=lambda self: fields.Datetime.now(), readonly=True)
    supervisor_id = supervisor_id = fields.Many2one('res.users', string="Supervisor", default=lambda self: self.env.user, readonly=True)