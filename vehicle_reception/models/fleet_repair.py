# -*- coding: utf-8 -*-

from odoo import models, fields, api

class FleetRepair(models.Model):
    _inherit = 'fleet.repair'

    recepcion_id = fields.Many2one('reception.vehicle', string="recepciones")
    recepciones_count = fields.Integer(string='Repair Orders', compute='_compute_repair_id')
    
    @api.depends('recepcion_id')
    def _compute_repair_id(self):
        for diagnose in self:
            recepciones_ids = self.env['reception.vehicle'].search([('reception_taller_id', '=', diagnose.id)])            
            diagnose.recepciones_count = len(recepciones_ids)