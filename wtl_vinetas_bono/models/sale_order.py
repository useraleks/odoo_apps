# -*- coding: utf-8 -*-

from odoo import fields, models, api, _

class SaleOrder(models.Model):
    _inherit = "sale.order"

    apply_for_vineta = fields.Boolean(string="aplica para Viñeta Bono")
    show_vineta_bono_warning = fields.Boolean(default=False, compute="_check_any_validation_vineta_bono")
    message_id = fields.Html()
    vineta_pricelist = fields.Many2one('product.pricelist', string="Tarifa de viñetas", compute="_get_customer_vineta_pricelist")
    no_client = fields.Boolean()
    count_vinetas = fields.Integer(string='Viñetas', compute='_compute_count_vinetas')

    def _compute_count_vinetas(self):
        for order in self:
            vinetas_ids = self.env['vineta.bono'].search([('origin_id', '=', order.id)])            
            order.count_vinetas = len(vinetas_ids)

    def button_view_vinetas_bono(self):
        list = []
        context = dict(self._context or {})
        vinetas_ids = self.env['vineta.bono'].search([('origin_id', '=', self.id)])           
        for order in vinetas_ids:
            list.append(order.id)
        return {
			'name': _('Vinetas bono'),
			'view_type': 'form',
			'view_mode': 'tree,form',
			'res_model': 'vineta.bono',
			'view_id': False,
			'type': 'ir.actions.act_window',
			'domain': [('id', 'in',list )],
			'context': context,
        }

    @api.depends('partner_id.apply_for_vineta', 'order_line')
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

            for line in rec.order_line:
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

    @api.depends('partner_id')
    def _get_customer_vineta_pricelist(self):
        for rec in self:
            if rec.partner_id and rec.partner_id.partner_pricelist_id:
                rec.vineta_pricelist = rec.partner_id.partner_pricelist_id
            else:
                 rec.vineta_pricelist = ''