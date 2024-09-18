# -*- coding: utf-8 -*-

from odoo import api, fields, models, _

class HrExpense(models.Model):
    _inherit = 'hr.expense'
    
    santotomas = fields.Boolean(string="santotomas")
    puertoquetzal = fields.Boolean('Puerto Quetzal', default=False)
    usuario = fields.Many2one('res.users', string="Empleado", default=lambda self: self.env.user)
    no_contenedor = fields.Char(string="Contenedor")
    
    @api.constrains('usuario')
    def _check_company(self):
        for record in self:
            if record.usuario.santotomas:
                record.santotomas = True
            if record.usuario.puertoquetzal:
                record.puertoquetzal = True

    @api.model
    def search(self, args, offset=0, limit=None, order=None, count=False):
        user = self.env.user

        if user.santotomas:
            args += [('santotomas', '=', True)]

        if user.puertoquetzal:
            args += [('puertoquetzal', '=', True)]

        return super(HrExpense, self).search(args, offset=offset, limit=limit, order=order, count=count)


class HrExpenseSheet(models.Model):
    _inherit = 'hr.expense.sheet'
    
    santotomas = fields.Boolean(related="expense_line_ids.santotomas", string="santotomas")
    puertoquetzal = fields.Boolean(related="expense_line_ids.puertoquetzal", string='Puerto Quetzal')
    usuario = fields.Many2one('res.users', string="Empleado", default=lambda self: self.env.user)
    no_contenedor = fields.Char(string="Contenedor", related="expense_line_ids.no_contenedor")

    @api.constrains('usuario')
    def _check_company(self):
        for record in self:
            if record.usuario.santotomas:
                record.santotomas = True
            if record.usuario.puertoquetzal:
                record.puertoquetzal = True

    @api.model
    def search(self, args, offset=0, limit=None, order=None, count=False):
        user = self.env.user

        if user.santotomas:
            args += [('santotomas', '=', True)]

        if user.puertoquetzal:
            args += [('puertoquetzal', '=', True)]

        return super(HrExpenseSheet, self).search(args, offset=offset, limit=limit, order=order, count=count)

