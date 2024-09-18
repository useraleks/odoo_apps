# -*- coding: utf-8 -*-

from odoo import fields, models, api, _
from odoo.exceptions import UserError, ValidationError

class VehicleReceptionLine(models.Model):
    _name = 'vehicle.reception.line'
    _description = "Vehicle Reception line"
    
    fleet_id = fields.Many2one('fleet.vehicle','Car', related='vehicle_reception_id.fleet_id')
    vehicle_reception_id = fields.Many2one('reception.vehicle', string='Car.', copy=False)
    license_plate = fields.Char('License Plate', related="fleet_id.license_plate")
    vin_sn= fields.Char('Chassis Number', related="fleet_id.vin_sn")
    model_id= fields.Many2one('fleet.vehicle.model', 'Model', related="fleet_id.model_id")
    
    @api.onchange('fleet_id')
    def onchange_fleet_id(self):
        addr = {}
        if self.fleet_id:
            fleet = self.fleet_id
            addr['license_plate'] = fleet.license_plate
            addr['vin_sn'] = fleet.vin_sn
            addr['model_id'] = fleet.model_id.id
        return {'value': addr}

    @api.constrains('vehicle_reception_id')
    def _check_unique_vehicle_reception_id(self):
        for record in self:
            if record.vehicle_reception_id and record.search_count([('vehicle_reception_id', '=', record.vehicle_reception_id.id)]) > 1:
                raise ValidationError("Solo puedes añadir un vehiculo.")