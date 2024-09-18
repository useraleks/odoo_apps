# -*- coding: utf-8 -*-

from odoo import fields, models, api, _

class CheckListLog(models.Model):
    _name = 'check.list.log'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _description = "CheckList"
    
    receipt_date = fields.Datetime(string='Date of Receipt', default=lambda self: fields.Datetime.now(), readonly=True)
    
    fleet_id = fields.Many2one('fleet.vehicle','Car')

    repair_checklist_documental_ids = fields.Many2many('fleet.repair.checklist.documental', 'repair_checklist_documental_log_rel',
                                                       'repair_id', 'checklist_id',
                                                       string='Repair Checklist Documental', required=True)
    repair_checklist_piloto_ids = fields.Many2many('fleet.repair.checklist.piloto', 'repair_checklist_piloto_log_rel',
                                                       'repair_id', 'checklist_id',
                                                       string='Repair Checklist Documental', required=True)
    repair_checklist_exterior_ids = fields.Many2many('fleet.repair.checklist.exterior', 'repair_checklist_exterior_log_rel',
                                                       'repair_id', 'checklist_id',
                                                       string='Repair Checklist Documental', required=True)
    repair_checklist_interior_ids = fields.Many2many('fleet.repair.checklist.interior', 'repair_checklist_interior_log_rel',
                                                       'repair_id', 'checklist_id',
                                                       string='Repair Checklist Interior', required=True)
    repair_checklist_complementos_ids = fields.Many2many('fleet.repair.checklist.complementos', 'repair_checklist_complementos_log_rel',
                                                       'repair_id', 'checklist_id',
                                                       string='Repair Checklist Complementos', required=True)
    repair_checklist_tanque_ids = fields.Many2many('fleet.repair.checklist.tanque', 'repair_checklist_tanque_log_rel',
                                                       'repair_id', 'checklist_id',
                                                       string='Repair Checklist Tanque', required=True)
    repair_checklist_chasis_ids = fields.Many2many('fleet.repair.checklist.chasis', 'repair_checklist_chasis_log_rel',
                                                       'repair_id', 'checklist_id',
                                                       string='Repair Checklist chasis', required=True)
    driver = fields.Many2one('hr.employee', string="Piloto")
    ref_reception = fields.Many2one('reception.vehicle', string="Ref en recepcion")
    ref_taller = fields.Many2one('reception.vehicle', string="Ref en taller")
    supervisor_id = supervisor_id = fields.Many2one('res.users', string="Supervisor", default=lambda self: self.env.user, readonly=True)