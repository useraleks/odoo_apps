# -*- coding: utf-8 -*-

from odoo import api, fields, models, _
from odoo.exceptions import ValidationError

class FleetRepairLine(models.Model):
    _inherit = 'fleet.repair.line'
    
    fleet_id = fields.Many2one('fleet.vehicle','Car', required=True)
    santotomas_line = fields.Boolean(string="Santo Tomas")
    puertoquetzal_line = fields.Boolean(string="Puerto Quetzal")
    fleet_repair_line = fields.One2many('fleet.repair.line', 'fleet_repair_id', string="Car Lines", required=True)
    service_type_ok = fields.Many2one('fleet.service.type', string="Tipo de servicio", related='fleet_repair_id.type_of_service')
    est_ser_hour= fields.Float(string='Estimated Sevice Hours')
    fuel_type= fields.Selection([('gasoline', 'Gasoline'), ('diesel', 'Diesel'), ('lpg', 'LPG'), ('electric', 'Electric'), ('hybrid', 'Hybrid')], 'Fuel Type', related="fleet_id.fuel_type")
    
    @api.onchange('fleet_id')
    def onchange_fleet_id_(self):
        for record in self:
            if record.fleet_repair_id.santotomascar == True:
                record.santotomas_line = True
            if record.fleet_repair_id.puertoquetzalcar == True:
                record.puertoquetzal_line = True
            addr = {}
            if self.fleet_id:
                fleet = self.fleet_id
                addr['license_plate'] = fleet.license_plate
                addr['vin_sn'] = fleet.vin_sn
                addr['fuel_type'] = fleet.fuel_type
                addr['model_id'] = fleet.model_id.id
            return {'value': addr}

    @api.constrains('fleet_repair_id')
    def _check_unique_fleet_repair_id(self):
        for record in self:
            if record.fleet_repair_id and record.search_count([('fleet_repair_id', '=', record.fleet_repair_id.id)]) > 1:
                raise ValidationError("Solo puedes añadir un vehiculo.")