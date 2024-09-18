# -*- coding: utf-8 -*-

# from odoo import models, fields, api


# class custom_search_renting(models.Model):
#     _name = 'custom_search_renting.custom_search_renting'
#     _description = 'custom_search_renting.custom_search_renting'

#     name = fields.Char()
#     value = fields.Integer()
#     value2 = fields.Float(compute="_value_pc", store=True)
#     description = fields.Text()
#
#     @api.depends('value')
#     def _value_pc(self):
#         for record in self:
#             record.value2 = float(record.value) / 100
