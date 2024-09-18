# -*- coding: utf-8 -*-

from odoo import api, fields, models, _
from odoo.exceptions import UserError, ValidationError

class ResCompany(models.Model):
    _inherit = 'res.company'

    cuenta_gastos = fields.Many2one(
        'account.account',
        string="Cuenta de gasto",
        readonly=False,
    )
    cuenta_x_pagar = fields.Many2one(
        'account.account',
        string="Cuenta por pagar",
        readonly=False,
    )

class ResConfigSettingsVineta(models.TransientModel):
    _inherit = 'res.config.settings'

    cuenta_gastos = fields.Many2one(
        'account.account',
        string="Credito",
        readonly=False,
        config_parameter='wtl_vinetas_bono.cuenta_gastos'
    )

    cuenta_x_pagar = fields.Many2one(
        'account.account',
        string="Debito",
        readonly=False,
        config_parameter='wtl_vinetas_bono.cuenta_x_pagar'
    )