# -*- coding: utf-8 -*-
# from odoo import http


# class CustomSearchRenting(http.Controller):
#     @http.route('/custom_search_renting/custom_search_renting', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/custom_search_renting/custom_search_renting/objects', auth='public')
#     def list(self, **kw):
#         return http.request.render('custom_search_renting.listing', {
#             'root': '/custom_search_renting/custom_search_renting',
#             'objects': http.request.env['custom_search_renting.custom_search_renting'].search([]),
#         })

#     @http.route('/custom_search_renting/custom_search_renting/objects/<model("custom_search_renting.custom_search_renting"):obj>', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('custom_search_renting.object', {
#             'object': obj
#         })
