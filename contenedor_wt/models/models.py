# -*- coding: utf-8 -*-

# from odoo import models, fields, api


# class contenedor_wt(models.Model):
#     _name = 'contenedor_wt.contenedor_wt'
#     _description = 'contenedor_wt.contenedor_wt'

#     name = fields.Char()
#     value = fields.Integer()
#     value2 = fields.Float(compute="_value_pc", store=True)
#     description = fields.Text()
#
#     @api.depends('value')
#     def _value_pc(self):
#         for record in self:
#             record.value2 = float(record.value) / 100
