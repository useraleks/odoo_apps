# -*- coding: utf-8 -*-

from odoo import models, fields, api

class FleetDiagnose(models.Model):
    _inherit = 'fleet.diagnose'

    contact_name = fields.Many2one('hr.employee', string='Contact Name', domain=[('is_driver', '=', True)], related="fleet_repair_id.contact_name", readonly=True)
    mechanic_id = fields.Many2one('hr.employee', string='Tecnico')
    santotomascar = fields.Boolean(string="santotomas", related="fleet_repair_id.santotomascar")
    puertoquetzalcar = fields.Boolean('Puerto Quetzal', default=False, related="fleet_repair_id.puertoquetzalcar")
    service_type_ok = fields.Many2one('fleet.service.type', string="Tipo de servicio", required=True, related='fleet_repair_id.type_of_service')
    vehiculo_id = fields.Many2one('fleet.vehicle', string='Car')
    service_id = fields.Many2one('fleet.vehicle.log.services', string='Servicio ID', copy=False)


    @api.model
    def search(self, args, offset=0, limit=None, order=None, count=False):
        user = self.env.user
        
        if user.santotomascar:
            args += [('santotomascar', '=', True)]
            
        if user.puertoquetzalcar:
            args += [('puertoquetzalcar', '=', True)]
            
        return super(FleetDiagnose, self).search(args, offset=offset, limit=limit, order=order, count=count)