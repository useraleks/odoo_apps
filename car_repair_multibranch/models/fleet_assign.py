# -*- coding: utf-8 -*-

from odoo import models, fields, api

class FleetDiagnoseAssigntoTechnician(models.TransientModel):
  _inherit = 'fleet.diagnose.assignto.technician'
  
  mechanic_id = fields.Many2one('hr.employee', string='Tecnico', required=True)
  santotomas_line = fields.Boolean(string="Santo Tomas")
  puertoquetzal_line = fields.Boolean(string="Puerto Quetzal")
  
  @api.model
  def default_get(self, fields):
    defaults = super(FleetDiagnoseAssigntoTechnician, self).default_get(fields)
    user = self.env.user
    if user.santotomascar:
      defaults['santotomas_line'] = user.santotomascar
    if user.puertoquetzalcar:
      defaults['puertoquetzal_line'] = user.puertoquetzalcar
    return defaults

  def do_assign_technician(self):
    self.env['fleet.diagnose'].browse(self._context.get('active_id')).write({'mechanic_id': self.mechanic_id.id, 'state': 'in_progress'})
    return {'type': 'ir.actions.act_window_close'}