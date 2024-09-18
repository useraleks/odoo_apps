# -*- coding: utf-8 -*-
# from odoo import http


# class ContenedorWt(http.Controller):
#     @http.route('/contenedor_wt/contenedor_wt', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/contenedor_wt/contenedor_wt/objects', auth='public')
#     def list(self, **kw):
#         return http.request.render('contenedor_wt.listing', {
#             'root': '/contenedor_wt/contenedor_wt',
#             'objects': http.request.env['contenedor_wt.contenedor_wt'].search([]),
#         })

#     @http.route('/contenedor_wt/contenedor_wt/objects/<model("contenedor_wt.contenedor_wt"):obj>', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('contenedor_wt.object', {
#             'object': obj
#         })
