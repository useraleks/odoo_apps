# -*- coding: utf-8 -*-

from odoo import models, fields, api

class FleetVehicle(models.Model):
	_inherit = 'fleet.vehicle'
	
	check_count = fields.Integer(string='CheckLists', compute='_compute_open_checklists')
	
	def _compute_open_checklists(self):
		for fleet in self:
			checklist_ids = self.env['check.list.log'].search([('fleet_id', '=', fleet.id)])
			fleet.check_count = len(checklist_ids)
			
	def view_checklists(self):
		list = []
		context = dict(self._context or {})
		return {
			'view_type': 'form',
			'view_mode': 'tree,form',
			'res_model': 'check.list.log',
			'view_id': False,
			'type': 'ir.actions.act_window',
			'domain': [('fleet_id', '=', self.id)],
			'context': context,
			}