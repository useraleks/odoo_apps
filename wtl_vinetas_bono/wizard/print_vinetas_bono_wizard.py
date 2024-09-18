# -*- coding: utf-8 -*-

from typing import List

from odoo import api, fields, models, _
from odoo.exceptions import UserError, ValidationError
from odoo.addons.base.models.res_partner import _lang_get
import logging

_logger = logging.getLogger(__name__)

class PrintVinetasBonoWizard(models.TransientModel):
	_name = 'print.vinetas.bono.wizard'
	_description = "Print Vinetas Bono Wizard"

	def get_partner_id(self):
		order = self.env['stock.picking'].browse(self._context.get('active_id'))
		if order:
			return order.partner_id
	
	partner_id = fields.Many2one('res.partner', string="Cliente", default=get_partner_id)
	is_printed= fields.Boolean(string="Se ha impreso ya?")
	output = fields.Selection(
        selection=[('pdf', 'PDF')],
        string='Print to',
        default='pdf',
    )
	user_id = fields.Many2one('res.users', string='Generado por', default=lambda self: self.env.user)
	origin_id = fields.Many2one('sale.order', string="Origen de la viñeta", default=lambda self: self._context.get('active_id.group_id'))
	products_line = fields.One2many('print.vinetas.bono.wizard.line', 'print_wizard', string=' Productos ')
	#campo que almacenara los registros creados
	label_ids = fields.One2many(
        comodel_name='generated.registries.vinetas',
        inverse_name='wizard_id',
        string='Labels for Vinetas',
    )
	report_id = fields.Many2one(
        comodel_name='ir.actions.report',
        string='Formato',
        domain=[('model', '=', 'print.vinetas.bono.wizard')],
    )
	
	def _convert_to_hex(self, sequence):
		return format(int(sequence), 'X').zfill(6)

	def get_labels_to_print(self):
		self.ensure_one()
		labels = self.label_ids
		if not labels:
			raise UserError(
				_('No hay viñetas para imprimir'))
		return labels
	
	def cancel_vinetas_bono(self):
		vineta_bono_model = self.env['vineta.bono']
		wizard_obj = self.env['print.vinetas.bono.wizard'].browse(self._ids[0])
		orders = self._context.get('active_id')
		picking_record = self.env['stock.picking'].browse(orders)
		pricelist = wizard_obj.partner_id.partner_pricelist_id
		
		for rec in self:
			for line in picking_record.label_ids:
				line.vineta_id.state = 'defeated'

		rec_ids = []
		for line in wizard_obj.products_line:
				if line.no_vinetas >= 1:
					veces = line.no_vinetas
					while veces != 0:
						vineta_vals = {
							'partner_id': wizard_obj.partner_id.id,
							'origin_id': picking_record.sale_id.id,
							'delivery_order': picking_record.id,
							'product_id': line.product_id.id,
							'date_end': line.date_end,
							'lot_id': line.lot_id.id,
							'name': self.env['ir.sequence'].next_by_code('vineta.bono') or _('New'),
							'barcode': self._convert_to_hex(self.env['ir.sequence'].next_by_code('vineta.bono.barcode') or _('New')),
						}
						# Buscar el precio del producto en la lista de precios del contacto
						price = line.product_id.vineta_cost
						for item in pricelist.item_ids:
							if item.product_tmpl_id.id == line.product_id.id:
								price = item.fixed_price
								break

						vineta_vals['price'] = price

						vineta = vineta_bono_model.create(vineta_vals)
						rec_ids.append((0, 0, {'vineta_id': vineta.id}))
						veces -= 1

		self.label_ids = rec_ids
		picking_record.label_ids = rec_ids
	
	def crear_asientos_contables(self):
		debito = self.env['ir.config_parameter'].sudo().get_param('wtl_vinetas_bono.cuenta_x_pagar')
		credito = self.env['ir.config_parameter'].sudo().get_param('wtl_vinetas_bono.cuenta_gastos')
		
		if not debito:
			raise ValidationError(_('No se ha configurado una cuenta de debito para los asientos'))
			
		if not credito:
			raise ValidationError(_('No se ha configurado una cuenta de credito para los asientos'))

		for rec in self:
			wizard_obj = self.env['print.vinetas.bono.wizard'].browse(self._ids[0])
			pricelist = wizard_obj.partner_id.partner_pricelist_id
			lineas_asiento = []  

			for line in rec.products_line:
				ref = f"Entrega de viñetas {line.product_id.name}"

				credit_value = {
					'name': 'Production Overheads',
					'debit': 0.0,
					'account_id': 15,
					'name': credito,
				}

				debit_value = {
					'name': 'Production Overheads',
					'credit': 0.0,
					'name': ref,
					'account_id': debito,
				}
				
				price = line.product_id.vineta_cost * line.no_vinetas
				for item in pricelist.item_ids:
					if item.product_tmpl_id.name == line.product_id.name:
						price = item.fixed_price * line.no_vinetas
						break

				debit_value['debit'] = price
				credit_value['credit'] = price

				lineas_asiento.append((0, 0, debit_value))
				lineas_asiento.append((0, 0, credit_value))

			vals = {
				'branch_id': 1,
				'journal_id': 35,
				'ref': f"Entrega de viñetas {rec.id}",
				'line_ids': lineas_asiento,
			}
			
			asiento_id = self.env['account.move'].create(vals)
			asiento_id.action_post()


	def crear_asientos_contables_reversibles(self):
		debito = self.env['ir.config_parameter'].sudo().get_param('wtl_vinetas_bono.cuenta_x_pagar')
		credito = self.env['ir.config_parameter'].sudo().get_param('wtl_vinetas_bono.cuenta_gastos')
		
		if not debito:
			raise ValidationError(_('No se ha configurado una cuenta de debito para los asientos'))
			
		if not credito:
			raise ValidationError(_('No se ha configurado una cuenta de credito para los asientos'))
		for rec in self:
			for line in rec.products_line:
				
				ref = f"devolucion de viñetas"
				
				credit_value = {
                    'name': 'Production Overheads',
                    'debit': 0.0,
                    'credit': line.no_vinetas,
                    'account_id': credito,
                    'name': ref,
                }
				
				debit_value = {
                    'name': 'Production Overheads',
                    'debit': line.no_vinetas,
                    'credit': 0.0,
                    'name': ref,
                    'account_id': debito,
                }
				
				
				vals = {
                    'branch_id' : 1,
                    'journal_id' : 35,
                    'ref' : ref,
                    'ref' : ref,
                    'line_ids': [(0, 0, credit_value),(0, 0, debit_value)],
                }
				asiento_id = self.env['account.move'].create(vals)
				asiento_id.action_post()


	#CREATE REGISTRIES ON 'vinetas.bono' MODEL
	def create_vinetas_bono_registries(self):
		vineta_bono_model = self.env['vineta.bono']
		wizard_obj = self.env['print.vinetas.bono.wizard'].browse(self._ids[0])
		orders = self._context.get('active_id')
		picking_record = self.env['stock.picking'].browse(orders)
		pricelist = wizard_obj.partner_id.partner_pricelist_id

		rec_ids = []
		if not picking_record.is_already_printed and picking_record.count_vinetas < 1:
			for line in wizard_obj.products_line:
				if line.no_vinetas >= 1:
					if line.is_blister == False:
						veces = line.no_vinetas
						while veces != 0:
							vineta_vals = {
								'partner_id': wizard_obj.partner_id.id,
								'origin_id': picking_record.sale_id.id,
								'delivery_order': picking_record.id,
								'product_id': line.product_id.id,
								'date_end': line.date_end,
								'lot_id': line.lot_id.id,
								'name': self._convert_to_hex(self.env['ir.sequence'].next_by_code('vineta.bono.barcode') or _('New')),
								'barcode': self.env['ir.sequence'].next_by_code('vineta.bono.barcode') or _('New'),
							}
							# Buscar el precio del producto en la lista de precios del contacto
							price = line.product_id.vineta_cost
							for item in pricelist.item_ids:
								if item.product_tmpl_id.name == line.product_id.name:
									price = item.fixed_price
									break

							vineta_vals['price'] = price

							vineta = vineta_bono_model.create(vineta_vals)
							rec_ids.append((0, 0, {'vineta_id': vineta.id}))
							veces -= 1

					if line.is_blister == True:
						veces = line.no_vinetas * line.product_id.blister_por_caja_id
						
						price = line.product_id.vineta_cost
						for item in pricelist.item_ids:
							if item.product_tmpl_id.name == line.product_id.name:
								price = item.fixed_price
								break

						precio_vineta = (price * line.no_vinetas) / veces
						
						while veces != 0:
							vineta_vals = {
								'partner_id': wizard_obj.partner_id.id,
								'origin_id': picking_record.sale_id.id,
								'delivery_order': picking_record.id,
								'product_id': line.product_id.id,
								'date_end': line.date_end,
								'lot_id': line.lot_id.id,
								'name': self._convert_to_hex(self.env['ir.sequence'].next_by_code('vineta.bono.barcode') or _('New')),
								'barcode': self.env['ir.sequence'].next_by_code('vineta.bono.barcode') or _('New'),
								'price': precio_vineta  # Asignar el mismo precio a todas las viñetas
							}
							
							vineta = vineta_bono_model.create(vineta_vals)
							rec_ids.append((0, 0, {'vineta_id': vineta.id}))
							veces -= 1

					self.label_ids = rec_ids
					picking_record.label_ids = rec_ids
					self.crear_asientos_contables()

		if not picking_record.is_already_printed and picking_record.count_vinetas > 0:
			return self.env.ref('wtl_vinetas_bono.action_report_product_label_A4_57x35_vineta').report_action(self)
		if picking_record.is_already_printed:
			raise ValidationError("Estas viñetas ya se han impreso, por favor pida autorizacion utilizar la ReImpresion")



	def print_vinetas_bono(self):
		orders = self._context.get('active_id')
		picking_record = self.env['stock.picking'].browse(orders)

		self.create_vinetas_bono_registries()

		picking_record.is_already_printed = True
		picking_record.is_already_records = True
		return self.env.ref('wtl_vinetas_bono.action_report_product_label_A4_57x35_vineta').report_action(self)
		#return self.env.ref('wtl_vinetas_bono.action_vinetas_bono_report').report_action(self)
	
	@api.model
	def default_get(self, fields):
			rec = super(PrintVinetasBonoWizard, self).default_get(fields)
			orders = self._context.get('active_id')
			order_lines = self.env['stock.picking'].browse(orders).move_line_ids_without_package
			exlines = []
			for line in order_lines:
				if line.product_id.apply_for_vineta == True and float(line.product_id.vineta_price_min) <= float(line.sale_price):
					exlines.append((0, 0, {
						'ro_line_id': line.id,
						'product_id': line.product_id.id,
						'lot_id': line.lot_id.id,
						'no_vinetas': line.invoiced,
						'date_end': line.lot_id.expiration_date,
					}))
			rec.update({'products_line': exlines})
			return rec
		
class PrintVinetasBonoWizardLine(models.TransientModel):
	_name = 'print.vinetas.bono.wizard.line'
	_description = "Print Vinetas Bono Wizard Lines"

	@api.depends('print_wizard.date_end')
	def get_expiry_date(self):
		order = self.print_wizard
		if order:
			return order.date_end

	product_id = fields.Many2one('product.product', string='Producto')
	ro_line_id = fields.Many2one('stock.move.line', string='Lineas de orden')
	no_vinetas = fields.Integer(string='No. Viñetas', digits='Cantidad de viñetas a imprimir', default=1.0)
	price_unit = fields.Float(string='Precio Unitario Viñetas', digits='Precio unitario de viñetas', default=0.0, compute="get_price_unit_vineta")
	print_wizard = fields.Many2one('print.vinetas.bono.wizard', string='Wizard')
	date_end = fields.Datetime(string="Fecha Expiracion", default=get_expiry_date)
	lot_id = fields.Many2one('stock.lot', string="Lote")
	is_blister = fields.Boolean(string="Particion en blisters?")

	@api.onchange('is_blister')
	def get_price_unit_vineta(self):
		pricelist = self.print_wizard.partner_id.partner_pricelist_id
		for rec in self:
				price = rec.product_id.vineta_cost
				for item in pricelist.item_ids:
					if item.product_tmpl_id.name == rec.product_id.name:
						price = item.fixed_price
						break
				veces = rec.no_vinetas * rec.product_id.blister_por_caja_id
				if rec.is_blister == True:
					if rec.product_id.blister_por_caja_id > 0:
						precio_vineta = (price * rec.no_vinetas) / veces
					else:
						raise ValidationError(_('No se ha configurado el blister por caja en el producto'))
				else:
					precio_vineta = price
				rec.price_unit = precio_vineta

class GeneratedRegistriesVinetas(models.TransientModel):
	_name = "generated.registries.vinetas"
	_description = 'Line with vinetas bono registries'
	_order = 'sequence'

	sequence = fields.Integer(default=900)
	selected = fields.Boolean(string='Print', default=True)
	wizard_id = fields.Many2one(comodel_name='print.vinetas.bono.wizard')  # Not make required
	vineta_id = fields.Many2one(comodel_name='vineta.bono', string="Viñeta")
	product_id = fields.Many2one(comodel_name='product.product', required=True, compute="_compute_product_id")
	barcode = fields.Char(compute='_compute_barcode')
	
	@api.depends('vineta_id')
	def _compute_barcode(self):
		for label in self:
			label.barcode = label.vineta_id.barcode	    
	
	@api.depends('vineta_id')
	def _compute_product_id(self):
	    for label in self:
		    label.product_id = label.vineta_id.product_id.id