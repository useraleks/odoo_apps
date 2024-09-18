# -*- coding: utf-8 -*-

from odoo import api, fields, models, _

class ProductTemplate(models.Model):
    _inherit = "product.template"

    need_prescription = fields.Boolean(string="¿Se necesita Receta?")