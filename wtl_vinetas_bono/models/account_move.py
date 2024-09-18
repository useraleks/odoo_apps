# -*- coding: utf-8 -*-

from odoo import fields, models, api, _

class AccountMove(models.Model):
    _inherit = "account.move"

    apply_for_vineta = fields.Boolean(string="aplica para Viñeta Bono")
    show_vineta_bono_warning = fields.Boolean(default=False, compute="_check_any_validation_vineta_bono")
    message_id = fields.Html()
    sale_id = fields.Many2one('sale.order', string="Sale", related="line_ids.sale_line_ids.order_id")
    no_client = fields.Boolean()
    count_vinetas = fields.Integer(string='Viñetas', compute='_compute_count_vinetas')

    @api.onchange('partner_id.apply_for_vineta', 'invoice_line_ids')
    def _check_any_validation_vineta_bono(self):
        for rec in self:
            #booleans
            no_client = False
            no_product = False
            no_price_min = False
            
            mensaje = ""
            productos_activos = []
            productos_min = []
            products_list_no_activos = ""
            products_list_no_min = ""

            if rec.partner_id.apply_for_vineta == False:
                no_client = True
            else:
                mensaje = "El cliente aplica para viñeta<br/>"
                no_client = False

            for line in rec.invoice_line_ids:
                if line.product_id.apply_for_vineta == True and float(line.product_id.vineta_price_min) <= float(line.price_unit):
                    productos_activos.append(line.product_id.name)
                    no_product = True
                else:
                    no_product = False

            if no_client == False:
                rec.show_vineta_bono_warning = True
            else:
                rec.show_vineta_bono_warning = False

            if productos_activos:
                products_list_no_activos = ', '.join(productos_activos)
                mensaje += f"Productos activos y cumplen con precio minimo {products_list_no_activos}<br/>"
            rec.message_id = mensaje