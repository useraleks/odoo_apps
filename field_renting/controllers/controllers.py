# -*- coding: utf-8 -*-
# from odoo import http


# class FieldRenting(http.Controller):
#     @http.route('/field_renting/field_renting', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/field_renting/field_renting/objects', auth='public')
#     def list(self, **kw):
#         return http.request.render('field_renting.listing', {
#             'root': '/field_renting/field_renting',
#             'objects': http.request.env['field_renting.field_renting'].search([]),
#         })

#     @http.route('/field_renting/field_renting/objects/<model("field_renting.field_renting"):obj>', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('field_renting.object', {
#             'object': obj
#         })
