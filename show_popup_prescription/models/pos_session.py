# -*- coding: utf-8 -*-

from odoo import api, fields, models, _

class PosSession(models.Model):
    _inherit = "pos.session"

    def _loader_params_product_product(self):

        res = super()._loader_params_product_product()
        res.get("search_params").get("fields").append('need_prescription')

        return res