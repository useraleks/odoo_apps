# -*- coding: utf-8 -*-

from odoo import fields, models, api, _

class ProductPricelist(models.Model):
    _inherit = "product.pricelist"

    is_for_vineta = fields.Boolean(string="Viñeta bono")