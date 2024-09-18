# -*- coding: utf-8 -*-res.users

from odoo import api, fields, models, _
from odoo.exceptions import ValidationError

class FleetRepair(models.Model):
    _inherit = 'fleet.repair'
    
    santotomascar = fields.Boolean(string="santotomas")
    puertoquetzalcar = fields.Boolean('Puerto Quetzal', default=False)
    motivo = fields.Selection([('Cabezal', 'Recepción de cabezal'), ('Chasis', 'Recepción de chasis')], string="Cabezal / Chasis", required=True)
    fleet_id = fields.Many2one('fleet.vehicle', string='Car')
    client_id = fields.Many2one('res.partner', string='Client', required=True , tracking=True, default=lambda self: self.env.user.comp_rama.partner_id, readonly=True)
    receipt_date = fields.Datetime(string='Date of Receipt', default=lambda self: fields.Datetime.now(), readonly=True)
    contact_name = fields.Many2one('hr.employee', string='Contact Name', domain=[('is_driver', '=', True)], required=True)
    phone = fields.Char(string='Contact Number', related="contact_name.mobile_phone", readonly=True)
    repair_checklist_ids = fields.Many2many('fleet.repair.checklist', 'repair_checklist_rel',
                                            'repair_id', 'checklist_id',
                                            string='Repair Checklist', required=True)
                                            
    repair_checklist_documental_ids = fields.Many2many('fleet.repair.checklist.documental', 'repair_checklist_documental_rel',
                                                       'repair_id', 'checklist_id',
                                                       string='Repair Checklist Documental', required=True)
    repair_checklist_piloto_ids = fields.Many2many('fleet.repair.checklist.piloto', 'repair_checklist_piloto_rel',
                                                       'repair_id', 'checklist_id',
                                                       string='Repair Checklist Documental', required=True)
    repair_checklist_exterior_ids = fields.Many2many('fleet.repair.checklist.exterior', 'repair_checklist_exterior_rel',
                                                       'repair_id', 'checklist_id',
                                                       string='Repair Checklist Documental', required=True)
    repair_checklist_interior_ids = fields.Many2many('fleet.repair.checklist.interior', 'repair_checklist_interior_rel',
                                                       'repair_id', 'checklist_id',
                                                       string='Repair Checklist Interior', required=True)
    repair_checklist_complementos_ids = fields.Many2many('fleet.repair.checklist.complementos', 'repair_checklist_complementos_rel',
                                                       'repair_id', 'checklist_id',
                                                       string='Repair Checklist Complementos', required=True)
    repair_checklist_tanque_ids = fields.Many2many('fleet.repair.checklist.tanque', 'repair_checklist_tanque_rel',
                                                       'repair_id', 'checklist_id',
                                                       string='Repair Checklist Tanque', required=True)
    repair_checklist_chasis_ids = fields.Many2many('fleet.repair.checklist.chasis', 'repair_checklist_chasis_rel',
                                                       'repair_id', 'checklist_id',
                                                       string='Repair Checklist chasis', required=True)
    gas = fields.Selection([('vacio', 'Tanque vacio'), ('medio', 'Medio'), ('lleno', 'Lleno')], string="Nivel de gasolina")
    llantas = fields.Char(string="Niveles de aire")
    chasis_abolladura = fields.Boolean(string="Abolladuras")
    chasis_abolladura_description = fields.Char(string="Descripcion")
    type_of_service = fields.Many2one('fleet.service.type', string="Tipo de servicio")
    vehiculo_id = fields.Many2one('fleet.vehicle', string="Vehiculo", related="fleet_repair_line.fleet_id")
    service_id = fields.Many2one('fleet.vehicle.log.services', string='Servicio ID', copy=False)
    odometer = fields.Float(string="Valor del odómetro", required=True, attrs={'readonly': [('is_from_reception_module', '=', True)]})
    odometer_id = fields.Many2one('fleet.vehicle.odometer', string='Car Odometer', copy=False)
    last_odometer = fields.Float(string="Ultimo odómetro", readonly=True, related="vehiculo_id.odometer")
    is_from_reception_module = fields.Boolean(string="Es desde recepcion de modulo?")
    
    @api.constrains('employee_id')
    def _check_company(self):
        for record in self:
            if record.employee_id.santotomascar:
                record.santotomascar = True
            if record.employee_id.puertoquetzalcar:
                record.puertoquetzalcar = True
                
    @api.constrains('repair_checklist_ids')
    def _check_repair_checklist_ids(self):
        for record in self:
            if not record.repair_checklist_piloto_ids:
                raise ValidationError("Lista de verificacion no puede estar vacia")
                
    @api.model
    def create(self, vals):
        if vals.get('name', _('New')) == _('New'):
            vals['name'] = self.env['ir.sequence'].next_by_code('fleet.repair') or _('New')
        res = super(FleetRepair, self).create(vals)
        return res
        
    @api.model
    def search(self, args, offset=0, limit=None, order=None, count=False):
        user = self.env.user

        if user.santotomascar:
            args += [('santotomascar', '=', True)]

        if user.puertoquetzalcar:
            args += [('puertoquetzalcar', '=', True)]

        return super(FleetRepair, self).search(args, offset=offset, limit=limit, order=order, count=count)
        
    @api.onchange('fleet_id')
    def _onchange_fleet_id(self):
        if self.fleet_id:
            line = self.fleet_repair_line.filtered(lambda r: r.fleet_id == self.fleet_id)
            if line:
                line.write({


                })
            else:
                self.fleet_repair_line = [(0, 0, {
                    'fleet_id': self.fleet_id.id,})]
        
    def action_print_checklist_id(self):
        return self.env.ref('car_repair_industry.fleet_repair_checklist_id').report_action(self)
        
    def action_create_fleet_diagnosis(self):
        Checklist_obj = self.env['check.list.log']
        Diagnosis_obj = self.env['fleet.diagnose']
        fleet_line_obj = self.env['fleet.repair.line']
        Service_obj = self.env['fleet.vehicle.log.services']
        repair_obj = self.env['fleet.repair'].browse(self._ids[0])
        mod_obj = self.env['ir.model.data']
        act_obj = self.env['ir.actions.act_window']
        if not repair_obj.fleet_repair_line:
            raise UserError('You cannot create Car Diagnosis without Cars.')
        if repair_obj.odometer < repair_obj.last_odometer:
            raise ValidationError('El odometro no puede ser menor que el ultimo odometro')
        if not repair_obj.type_of_service:
            raise ValidationError('Porfavor seleccione el tipo de servicio.')
        
        diagnose_vals = {
            'service_rec_no': repair_obj.sequence,
            'name': repair_obj.name,
            'priority': repair_obj.priority,
            'receipt_date': repair_obj.receipt_date,
            'client_id': repair_obj.client_id.id,
            'contact_name': repair_obj.contact_name,
            'phone': repair_obj.phone,
            'client_phone': repair_obj.client_phone,
            'client_mobile': repair_obj.client_mobile,
            'client_email': repair_obj.client_email,
            'fleet_repair_id': repair_obj.id,
            'vehiculo_id': repair_obj.fleet_id.id,
            'state': 'draft',
        }
        diagnose_id = Diagnosis_obj.create(diagnose_vals)
        service_vals = {
            'description': repair_obj.name,
            'service_type_id': repair_obj.type_of_service.id,
            'vehicle_id': repair_obj.vehiculo_id.id,
            'odometer': repair_obj.odometer,
            'piloto_id': repair_obj.contact_name.id,
            'id_reparacion': repair_obj.id
        }
        service_id = Service_obj.create(service_vals)
        for line in repair_obj.fleet_repair_line:
            fleet_line_vals = {
				'fleet_id': line.fleet_id.id,
				'license_plate': line.license_plate,
				'vin_sn': line.vin_sn,
				'fuel_type': line.fuel_type,
				'model_id': line.model_id.id,
				'service_type': line.service_type.id,
				'service_type_ok': line.service_type_ok.id,
				'guarantee': line.guarantee,
				'guarantee_type':line.guarantee_type,
				'service_detail': line.service_detail,
				'diagnose_id': diagnose_id.id,
				'state': 'diagnosis',
				'source_line_id': line.id,
			}
            fleet_line_obj.create(fleet_line_vals)
            line.write({'state': 'diagnosis'})

            reception_vals = {
                'fleet_id': repair_obj.fleet_id.id,
                'repair_checklist_piloto_ids': repair_obj.repair_checklist_piloto_ids,
                'repair_checklist_exterior_ids': repair_obj.repair_checklist_exterior_ids,
                'repair_checklist_documental_ids': repair_obj.repair_checklist_documental_ids,
                'repair_checklist_interior_ids': repair_obj.repair_checklist_interior_ids,
                'repair_checklist_complementos_ids': repair_obj.repair_checklist_complementos_ids,
                'repair_checklist_tanque_ids': repair_obj.repair_checklist_tanque_ids,
                'repair_checklist_chasis_ids': repair_obj.repair_checklist_chasis_ids,
                'driver': repair_obj.contact_name.id,
            }
            reception_id = Checklist_obj.create(reception_vals)
            
        self.write({'state': 'diagnosis', 'diagnose_id': diagnose_id.id, 'service_id': service_id.id})
        result = mod_obj._xmlid_lookup("%s.%s" % ('car_repair_industry', 'action_fleet_diagnose_tree_view'))[1:3]
        id = result and result[1] or False
        result = act_obj.browse(id).read()[0]
        res = mod_obj._xmlid_lookup("%s.%s" % ('car_repair_industry', 'view_fleet_diagnose_form'))[1:3]
        result['views'] = [(res and res[1] or False, 'form')]
        result['res_id'] = diagnose_id.id or False
        return result