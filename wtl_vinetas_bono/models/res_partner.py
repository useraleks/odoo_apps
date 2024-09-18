# -*- coding: utf-8 -*-

from odoo import fields, models, api, _

class ResPartner(models.Model):
    _inherit = "res.partner"

    apply_for_vineta = fields.Boolean(string="Viñeta Bono")
    partner_pricelist_id = fields.Many2one('product.pricelist' ,string="Lista de precios")
    count_vinetas = fields.Integer(string='Viñetas', compute='_compute_count_vinetas')

    def _compute_count_vinetas(self):
        for order in self:
            vinetas_ids = self.env['vineta.bono'].search([('partner_id', '=', order.id)])            
            order.count_vinetas = len(vinetas_ids)

    def button_view_vinetas_bono(self):
        list = []
        context = dict(self._context or {})
        vinetas_ids = self.env['vineta.bono'].search([('partner_id', '=', self.id)])           
        for order in vinetas_ids:
            list.append(order.id)
        return {
			'name': _('Vinetas bono'),
			'view_type': 'form',
			'view_mode': 'tree,form',
			'res_model': 'vineta.bono',
			'view_id': False,
			'type': 'ir.actions.act_window',
			'domain': [('id', 'in',list )],
			'context': context,
        }