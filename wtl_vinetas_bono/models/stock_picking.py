# -*- coding: utf-8 -*-

from odoo import fields, models, api, _
from odoo.exceptions import ValidationError
from odoo.addons.stock.models.stock_picking import Picking

class StockPicking(models.Model):
    _inherit = "stock.picking"

    label_ids = fields.One2many(
        comodel_name='generated.vinetas',
        inverse_name='wizard_id',
        string='Viñetas Generadas',
    )
    count_vinetas = fields.Integer(string='Viñetas', compute='_compute_count_vinetas')
    is_authorize = fields.Boolean(string='Autorizado?', default=False)

    def _compute_count_vinetas(self):
        for order in self:
            vinetas_ids = self.env['vineta.bono'].search([('delivery_order', '=', order.id)])            
            order.count_vinetas = len(vinetas_ids)

    def button_view_vinetas_bono(self):
        list = []
        context = dict(self._context or {})
        vinetas_ids = self.env['vineta.bono'].search([('delivery_order', '=', self.id)])           
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
    
    """def button_validate(self):
        res = super(StockPicking, self).button_validate()
        print("Funciona lo agregado")
        return res"""

    is_already_printed = fields.Boolean("Se ha impreso?")
    is_already_records = fields.Boolean("se han generado las viñetas ya?")
    show_vineta_bono_warning = fields.Boolean(default=False, compute="_check_any_validation_vineta_bono")
    message_id = fields.Html()
    show_print_button = fields.Boolean()
            

    @api.depends('partner_id.apply_for_vineta', 'sale_id.order_line', 'show_print_button')
    def _check_any_validation_vineta_bono(self):
        for rec in self:
            #booleans
            no_client = False
            no_product = False
            no_price_min = False
            
            mensaje = ""
            productos_activos = []
            productos_for_vineta = []
            productos_min = []
            products_list_no_activos = ""
            products_list_no_min = ""

            if rec.partner_id.apply_for_vineta == False:
                no_client = True
            else:
                rec.show_print_button = True
                mensaje = "El cliente aplica para viñeta<br/>"
                no_client = False

            for line in rec.sale_id.order_line:
                if line.product_id.apply_for_vineta == True and float(line.product_id.vineta_price_min) <= float(line.price_unit):
                    productos_activos.append(line.product_id.name)
                    productos_for_vineta.append(line.product_id.id)
                    no_product = True
                else:
                    no_product = False

            if no_client == False and rec.group_id:
                rec.show_vineta_bono_warning = True
            else:
                rec.show_vineta_bono_warning = False

            if productos_activos:
                products_list_no_activos = ', '.join(productos_activos)
                mensaje += f"Productos activos y cumplen con precio minimo {products_list_no_activos}<br/>"
            rec.message_id = mensaje
            return productos_for_vineta

    @api.model
    def create(self, vals):
        vals['is_authorize'] = False
        return super(StockPicking, self).create(vals)

    def copy(self, default=None):
        default = dict(default or {})
        default['is_authorize'] = False
        return super(StockPicking, self).copy(default)
        

class GeneratedVinetas(models.Model):
    _name = "generated.vinetas"
    _description = 'Generated Vinetas'
    _order = 'sequence'

    sequence = fields.Integer(default=900)
    wizard_id = fields.Many2one(comodel_name='stock.picking')  # Not make required
    vineta_id = fields.Many2one(comodel_name='vineta.bono', string="Viñeta")
    product_id = fields.Many2one(comodel_name='product.product', related="vineta_id.product_id")
    barcode = fields.Char(related="vineta_id.barcode")
    price = fields.Float(related="vineta_id.price", string="precio")
    state = fields.Selection([
        ('available', 'Disponible'),
        ('defeated', 'Anulado'),
        ('paid', 'Pagado'),
    ], string='Estado', index=True, default='available', tracking=True, related="vineta_id.state")