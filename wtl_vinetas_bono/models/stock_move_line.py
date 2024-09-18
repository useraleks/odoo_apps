# -*- coding: utf-8 -*-

from odoo import fields, models, api, _
from odoo.exceptions import ValidationError
from odoo.addons.stock.models.stock_picking import Picking

class StockMoveLine(models.Model):
    _inherit = "stock.move.line"

    invoiced = fields.Float(string="Facturado")