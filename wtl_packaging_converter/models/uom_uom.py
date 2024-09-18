# -*- coding: utf-8 -*-

from odoo import fields, models, api, _

class UomUom(models.Model):
    _inherit = "uom.uom"

    is_unit = fields.Boolean(string="Es unidad?")