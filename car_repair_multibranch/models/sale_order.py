# -*- coding: utf-8 -*-

from odoo import api, fields, models, _

class SaleOrderLine(models.Model):
    _inherit = 'sale.order.line'

    diagnose_fleet_ids = fields.Many2many(
        comodel_name='fleet.vehicle',
        compute='_compute_diagnose_fleet_ids',
        string='Diagnosis Fleets',
        store=True,
    )