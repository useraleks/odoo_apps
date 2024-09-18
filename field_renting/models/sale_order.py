# -*- coding: utf-8 -*-

from odoo import fields, models, api, _
from odoo.exceptions import ValidationError

class RentalOrder(models.Model):
    _inherit = 'sale.order'

    piloto_id_dos = fields.Many2one('res.partner', string="Piloto", related="cabezal_id.driver_id", readonly=True, store=True)