# -*- coding: utf-8 -*-

from odoo import fields, models, _
from odoo.exceptions import UserError

#Inspeccion Documental

class FleetRepairChecklistDocumental(models.Model):
    _name = 'fleet.repair.checklist.documental'
    _description = "FLEET REPAIR Checklist Documental"

    name = fields.Char('Nombre', required=True, translate=True)
    active = fields.Boolean(default=True)

    def unlink(self):
        fleet_repair_obj = self.env['fleet.repair']
        rule_ranges = fleet_repair_obj.search([('repair_checklist_documental_ids', 'in', self.ids)])
        if rule_ranges:
            raise UserError(
                _("You Are Trying To Delete a Record That Is Still Referenced!\nInstead Delete The Record Use Archive"))
        return super(FleetRepairChecklistDocumental, self).unlink()


#Datos del piloto

class FleetRepairChecklistPiloto(models.Model):
    _name = 'fleet.repair.checklist.piloto'
    _description = "FLEET REPAIR Checklist Piloto"

    name = fields.Char('Nombre', required=True, translate=True)
    active = fields.Boolean(default=True)

    def unlink(self):
        fleet_repair_obj = self.env['fleet.repair']
        rule_ranges = fleet_repair_obj.search([('repair_checklist_piloto_ids', 'in', self.ids)])
        if rule_ranges:
            raise UserError(
                _("You Are Trying To Delete a Record That Is Still Referenced!\nInstead Delete The Record Use Archive"))
        return super(FleetRepairChecklistPiloto, self).unlink()

#Exterior
class FleetRepairChecklistExterior(models.Model):
    _name = 'fleet.repair.checklist.exterior'
    _description = "FLEET REPAIR Checklist Exterior"

    name = fields.Char('Nombre', required=True, translate=True)
    active = fields.Boolean(default=True)

    def unlink(self):
        fleet_repair_obj = self.env['fleet.repair']
        rule_ranges = fleet_repair_obj.search([('repair_checklist_exterior_ids', 'in', self.ids)])
        if rule_ranges:
            raise UserError(
                _("You Are Trying To Delete a Record That Is Still Referenced!\nInstead Delete The Record Use Archive"))
        return super(FleetRepairChecklistExterior, self).unlink()


#Interior
class FleetRepairChecklistInterior(models.Model):
    _name = 'fleet.repair.checklist.interior'
    _description = "FLEET REPAIR Checklist Interior"

    name = fields.Char('Nombre', required=True, translate=True)
    active = fields.Boolean(default=True)

    def unlink(self):
        fleet_repair_obj = self.env['fleet.repair']
        rule_ranges = fleet_repair_obj.search([('repair_checklist_interior_ids', 'in', self.ids)])
        if rule_ranges:
            raise UserError(
                _("You Are Trying To Delete a Record That Is Still Referenced!\nInstead Delete The Record Use Archive"))
        return super(FleetRepairChecklistInterior, self).unlink()


#Complementos
class FleetRepairChecklistComplementos(models.Model):
    _name = 'fleet.repair.checklist.complementos'
    _description = "FLEET REPAIR Checklist Complementos"

    name = fields.Char('Nombre', required=True, translate=True)
    active = fields.Boolean(default=True)

    def unlink(self):
        fleet_repair_obj = self.env['fleet.repair']
        rule_ranges = fleet_repair_obj.search([('repair_checklist_complementos_ids', 'in', self.ids)])
        if rule_ranges:
            raise UserError(
                _("You Are Trying To Delete a Record That Is Still Referenced!\nInstead Delete The Record Use Archive"))
        return super(FleetRepairChecklistComplementos, self).unlink()

#TANQUE
class FleetRepairChecklistTanque(models.Model):
    _name = 'fleet.repair.checklist.tanque'
    _description = "FLEET REPAIR Checklist Tanque"

    name = fields.Char('Nombre', required=True, translate=True)
    active = fields.Boolean(default=True)

    def unlink(self):
        fleet_repair_obj = self.env['fleet.repair']
        rule_ranges = fleet_repair_obj.search([('repair_checklist_tanque_ids', 'in', self.ids)])
        if rule_ranges:
            raise UserError(
                _("You Are Trying To Delete a Record That Is Still Referenced!\nInstead Delete The Record Use Archive"))
        return super(FleetRepairChecklistTanque, self).unlink()


#CHASIS
class FleetRepairChecklistChasis(models.Model):
    _name = 'fleet.repair.checklist.chasis'
    _description = "FLEET REPAIR Checklist Chasis"

    name = fields.Char('Nombre', required=True, translate=True)
    active = fields.Boolean(default=True)

    def unlink(self):
        fleet_repair_obj = self.env['fleet.repair']
        rule_ranges = fleet_repair_obj.search([('repair_checklist_chasis_ids', 'in', self.ids)])
        if rule_ranges:
            raise UserError(
                _("You Are Trying To Delete a Record That Is Still Referenced!\nInstead Delete The Record Use Archive"))
        return super(FleetRepairChecklistChasis, self).unlink()

