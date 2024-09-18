# -*- coding: utf-8 -*-

from odoo import fields, models, api, _

class ProductTemplate(models.Model):
    _inherit = "product.template"

    apply_for_vineta = fields.Boolean(string="Viñeta Bono")
    vineta_cost = fields.Float(string="Costo de Viñeta")
    vineta_price_min = fields.Float(string="Precio de Viñeta Minimo")
    blister_por_caja_id = fields.Float(string="Blister por caja")