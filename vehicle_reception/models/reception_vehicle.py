# -*- coding: utf-8 -*-

from odoo import fields, models, api, _
from odoo.exceptions import UserError, ValidationError

class ReceptionVehicle(models.Model):
    _name = 'reception.vehicle'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _description = "Reception Vehicle"
    

    sequence = fields.Char(string='Sequence', readonly=True ,copy =False, default=lambda self: _('New'))
    santotomascar = fields.Boolean(string="santotomas")
    puertoquetzalcar = fields.Boolean('Puerto Quetzal', default=False)
    name = fields.Char(string='Asunto', required=True)
    motivo = fields.Selection([('Cabezal', 'Recepción de cabezal'), ('Chasis', 'Recepción de chasis')], string="Cabezal / Chasis", required=True)
    client_id = fields.Many2one('res.partner', string='Client', required=True, tracking=True, default=lambda self: self.env.user.comp_rama.partner_id, readonly=True)
    priority = fields.Selection([('0','Low'), ('1','Normal'), ('2','High')], 'Priority')
    driver = fields.Many2one('hr.employee', string="Driver", required=True)
    supervisor_id = fields.Many2one('res.users', string="Supervisor", default=lambda self: self.env.user, readonly=True)
    receipt_date = fields.Datetime(string='Date of Receipt', default=lambda self: fields.Datetime.now(), readonly=True)
    driver_phone = fields.Many2one('hr.employee', string='Driver Phone', domain=[('is_driver', '=', True)])
    driver_phone_id = fields.Char(string='Driver Phone', related="driver.mobile_phone", readonly=True)
    odometer = fields.Float(string="Valor del odómetro", required=True)
    last_odometer = fields.Float(string="Ultimo odómetro", readonly=True, related="fleet_id.odometer")
    vehicle_reception_line = fields.One2many('vehicle.reception.line', 'vehicle_reception_id', string="Reception Lines")
    vehicle_reception_line = fields.One2many('vehicle.reception.line', 'vehicle_reception_id', string="Car Lines")
    fleet_id = fields.Many2one('fleet.vehicle', string='Car', domain=[('state_id.sequence', '=', 2)], required=True)
    state = fields.Many2one('fleet.vehicle.state', related='fleet_id.state_id')
    repair_checklist_documental_ids = fields.Many2many('fleet.repair.checklist.documental', 'repair_checklist_documental_reception_rel',
                                                       'repair_id', 'checklist_id',
                                                       string='Repair Checklist Documental', required=True)
    repair_checklist_piloto_ids = fields.Many2many('fleet.repair.checklist.piloto', 'repair_checklist_piloto_reception_rel',
                                                       'repair_id', 'checklist_id',
                                                       string='Repair Checklist Documental', required=True)
    repair_checklist_exterior_ids = fields.Many2many('fleet.repair.checklist.exterior', 'repair_checklist_exterior_reception_rel',
                                                       'repair_id', 'checklist_id',
                                                       string='Repair Checklist Documental', required=True)
    repair_checklist_interior_ids = fields.Many2many('fleet.repair.checklist.interior', 'repair_checklist_interior_reception_rel',
                                                       'repair_id', 'checklist_id',
                                                       string='Repair Checklist Interior', required=True)
    repair_checklist_complementos_ids = fields.Many2many('fleet.repair.checklist.complementos', 'repair_checklist_complementos_reception_rel',
                                                       'repair_id', 'checklist_id',
                                                       string='Repair Checklist Complementos', required=True)
    repair_checklist_tanque_ids = fields.Many2many('fleet.repair.checklist.tanque', 'repair_checklist_tanque_reception_rel',
                                                       'repair_id', 'checklist_id',
                                                       string='Repair Checklist Tanque', required=True)
    repair_checklist_chasis_ids = fields.Many2many('fleet.repair.checklist.chasis', 'repair_checklist_chasis_reception_rel',
                                                       'repair_id', 'checklist_id',
                                                       string='Repair Checklist chasis', required=True)
                                                       
    is_state_sequence_1 = fields.Boolean(string="Is State Sequence 1", compute="_compute_is_state_sequence_1", store=True,)
    is_state_sequence_2 = fields.Boolean(string="Is State Sequence 2", compute="_compute_is_state_sequence_2", store=True,)
    selected_option = fields.Boolean(string="Opcion seleccionada?")
    is_from_reception_module = fields.Boolean(string="Es desde recepcion de modulo?", default=True)
    reception_taller_id = fields.Many2one('fleet.repair', string="Recepcion en taller", copy=False)
    dig_count  = fields.Integer(string='Taller', compute='_compute_reception_taller_id')
    description = fields.Text(string='Notas de la recepcion')
    
    @api.depends('fleet_id.state_id.sequence')
    def _compute_is_state_sequence_1(self):
        for record in self:
            record.is_state_sequence_1 = record.fleet_id.state_id.sequence == 1
            
    @api.depends('fleet_id.state_id.sequence')
    def _compute_is_state_sequence_2(self):
        for record in self:
            record.is_state_sequence_2 = record.fleet_id.state_id.sequence == 3
            
    @api.depends('reception_taller_id')
    def _compute_reception_taller_id(self):
        for order in self:
            dig_order_ids = self.env['fleet.repair'].search([('recepcion_id', '=', order.id)])            
            order.dig_count = len(dig_order_ids)

    @api.constrains('supervisor_id')
    def _check_company(self):
        for record in self:
            if record.supervisor_id.santotomascar:
                record.santotomascar = True
            if record.supervisor_id.puertoquetzalcar:
                record.puertoquetzalcar = True
            
    @api.constrains('repair_checklist_piloto_ids')
    def _check_repair_checklist_ids(self):
        for record in self:
            if not record.repair_checklist_piloto_ids:
                raise ValidationError("Lista de verificacion no puede estar vacia")
    
    @api.onchange('fleet_id')
    def _onchange_fleet_id(self):
        if self.fleet_id:
            line = self.vehicle_reception_line.filtered(lambda r: r.fleet_id == self.fleet_id)
            if line:
                line.write({

                })
            else:
                self.vehicle_reception_line = [(0, 0, {
                    'fleet_id': self.fleet_id.id,})]
                    
    @api.model
    def create(self, vals):
        if vals.get('sequence', _('New')) == _('New'):
            vals['sequence'] = self.env['ir.sequence'].next_by_code('reception.vehicle') or _('New')
        res = super(ReceptionVehicle, self).create(vals)
        return res

    @api.model
    def search(self, args, offset=0, limit=None, order=None, count=False):
        user = self.env.user

        if user.santotomascar:
            args += [('santotomascar', '=', True)]

        if user.puertoquetzalcar:
            args += [('puertoquetzalcar', '=', True)]

        return super(ReceptionVehicle, self).search(args, offset=offset, limit=limit, order=order, count=count)
        
    def action_pasar_siguiente_estado(self):
        Checklist_obj = self.env['check.list.log']
        odometer_obj = self.env['fleet.vehicle.odometer']
        reception_obj = self.env['reception.vehicle'].browse(self._ids[0])
        mod_obj = self.env['ir.model.data']
        act_obj = self.env['ir.actions.act_window']
        for rec in self:
            rec.selected_option = True
        next_state = self.env['fleet.vehicle.state'].search([
            ('sequence', '=', 1)
        ], limit=1)
        if next_state:
            self.fleet_id.state_id = next_state
            
        reception_vals = {
            'fleet_id': reception_obj.fleet_id.id,
            'driver': reception_obj.driver.id,
            'ref_reception': self.id,
            'repair_checklist_piloto_ids': reception_obj.repair_checklist_piloto_ids,
            'repair_checklist_exterior_ids': reception_obj.repair_checklist_exterior_ids,
            'repair_checklist_documental_ids': reception_obj.repair_checklist_documental_ids,
            'repair_checklist_interior_ids': reception_obj.repair_checklist_interior_ids,
            'repair_checklist_complementos_ids': reception_obj.repair_checklist_complementos_ids,
            'repair_checklist_tanque_ids': reception_obj.repair_checklist_tanque_ids,
            'repair_checklist_chasis_ids': reception_obj.repair_checklist_chasis_ids,
        }
        reception_id = Checklist_obj.create(reception_vals)
        if reception_obj.odometer < reception_obj.last_odometer:
            raise ValidationError('El odometro debe ser mayor o igual al ultimo odometro')
            
        odometer_vals = {
            'vehicle_id': reception_obj.fleet_id.id,
            'ref_reception': self.id,
            'driver': reception_obj.driver.id,
            'value': reception_obj.odometer,}
        odometer_id = odometer_obj.create(odometer_vals)
        
    def button_view_taller(self):
        list = []
        context = dict(self._context or {})
        dig_order_ids = self.env['fleet.repair'].search([('recepcion_id', '=', self.id)])           
        for order in dig_order_ids:
            list.append(order.id)
        return {
			'name': _('Taller'),
			'view_type': 'form',
			'view_mode': 'tree,form',
			'res_model': 'fleet.repair',
			'view_id': False,
			'type': 'ir.actions.act_window',
			'domain': [('id', 'in',list )],
			'context': context,
        }

    """def action_registrar_lista(self):
        Checklist_obj = self.env['check.list.log']
        odometer_obj = self.env['fleet.vehicle.odometer']
        reception_obj = self.env['reception.vehicle'].browse(self._ids[0])
        mod_obj = self.env['ir.model.data']
        act_obj = self.env['ir.actions.act_window']
        
        reception_vals = {
            'fleet_id': reception_obj.fleet_id.id,
            'repair_checklist_piloto_ids': reception_obj.repair_checklist_piloto_ids,
            'repair_checklist_exterior_ids': reception_obj.repair_checklist_exterior_ids,
            'repair_checklist_documental_ids': reception_obj.repair_checklist_documental_ids,
            'repair_checklist_interior_ids': reception_obj.repair_checklist_interior_ids,
            'repair_checklist_complementos_ids': reception_obj.repair_checklist_complementos_ids,
            'repair_checklist_tanque_ids': reception_obj.repair_checklist_tanque_ids,
            'repair_checklist_chasis_ids': reception_obj.repair_checklist_chasis_ids,
        }
        reception_id = Checklist_obj.create(reception_vals)
        if reception_obj.odometer < reception_obj.last_odometer:
            raise ValidationError('El odometro debe ser mayor o igual al ultimo odometro')
            
        odometer_vals = {
            'vehicle_id': reception_obj.fleet_id.id,
            'value': reception_obj.odometer,
        }
        odometer_id = odometer_obj.create(odometer_vals)"""
        
    def poner_en_taller(self):
        for rec in self:
            rec.selected_option = True
        next_state = self.env['fleet.vehicle.state'].search([
            ('sequence', '=', 3)
        ], limit=1)
        if next_state:
            self.fleet_id.state_id = next_state
            
        Reception_taller_obj = self.env['fleet.repair']
        Checklist_obj = self.env['check.list.log']
        reception_line_obj = self.env['vehicle.reception.line']
        odometer_obj = self.env['fleet.vehicle.odometer']
        fleet_line_obj = self.env['fleet.repair.line']
        reception_obj = self.env['reception.vehicle'].browse(self._ids[0])
        mod_obj = self.env['ir.model.data']
        act_obj = self.env['ir.actions.act_window']
        if not reception_obj.vehicle_reception_line:
            raise UserError('Debes llenar la linea de vehiculo.')
            
        reception_taller_vals = {
            'name': reception_obj.name,
            'motivo': reception_obj.motivo,
            'is_from_reception_module': reception_obj.is_from_reception_module,
            'fleet_id': reception_obj.fleet_id.id,
            'priority': reception_obj.priority,
            'client_id': reception_obj.client_id.id,
            'contact_name': reception_obj.driver.id,
            'odometer': reception_obj.odometer,
            'recepcion_id': reception_obj.id,
            'repair_checklist_piloto_ids': reception_obj.repair_checklist_piloto_ids,
            'repair_checklist_exterior_ids': reception_obj.repair_checklist_exterior_ids,
            'repair_checklist_documental_ids': reception_obj.repair_checklist_documental_ids,
            'repair_checklist_interior_ids': reception_obj.repair_checklist_interior_ids,
            'repair_checklist_complementos_ids': reception_obj.repair_checklist_complementos_ids,
            'repair_checklist_tanque_ids': reception_obj.repair_checklist_tanque_ids,
            'repair_checklist_chasis_ids': reception_obj.repair_checklist_chasis_ids,
        }
        reception_taller_id = Reception_taller_obj.create(reception_taller_vals)
        repair_line_vals = []
        for line in self.vehicle_reception_line:
            repair_line_vals = {
                'fleet_id': line.fleet_id.id,
                'license_plate': line.license_plate,
                'vin_sn': line.vin_sn,
                'model_id': line.model_id.id,
                'fleet_repair_id': reception_taller_id.id,
            }
            self.env['fleet.repair.line'].create(repair_line_vals)
        
        if reception_obj.odometer < reception_obj.last_odometer:
            raise ValidationError('El odometro debe ser mayor o igual al ultimo odometro')
            
        odometer_vals = {
            'vehicle_id': reception_obj.fleet_id.id,
            'value': reception_obj.odometer,
            'driver': reception_obj.driver.id,
            'ref_reception': self.id,
            }
        odometer_id = odometer_obj.create(odometer_vals)
        
        reception_vals = {
            'fleet_id': reception_obj.fleet_id.id,
            'repair_checklist_piloto_ids': reception_obj.repair_checklist_piloto_ids,
            'repair_checklist_exterior_ids': reception_obj.repair_checklist_exterior_ids,
            'repair_checklist_documental_ids': reception_obj.repair_checklist_documental_ids,
            'repair_checklist_interior_ids': reception_obj.repair_checklist_interior_ids,
            'repair_checklist_complementos_ids': reception_obj.repair_checklist_complementos_ids,
            'repair_checklist_tanque_ids': reception_obj.repair_checklist_tanque_ids,
            'repair_checklist_chasis_ids': reception_obj.repair_checklist_chasis_ids,
            'driver': reception_obj.driver.id,
            'ref_reception': self.id,
        }
        recepcion_id = Checklist_obj.create(reception_vals)

        self.write({'reception_taller_id': reception_taller_id.id})
        result = mod_obj._xmlid_lookup("%s.%s" % ('car_repair_industry', 'action_fleet_repair_tree_view'))[1:3]
        id = result and result[1] or False
        result = act_obj.browse(id).read()[0]
        res = mod_obj._xmlid_lookup("%s.%s" % ('car_repair_industry', 'view_fleet_repair_form'))[1:3]
        result['views'] = [(res and res[1] or False, 'form')]
        result['res_id'] = reception_taller_id.id or False
        return result