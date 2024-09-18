# -*- coding: utf-8 -*-

from odoo import fields, models

class AccountMoveLine(models.Model):
    _inherit = 'account.move.line'

    contenedor_x = fields.Char(
        string="Contenedor No",
        related='sale_line_ids.contenedor_no',
        readonly=True,
        store=True,
    )
