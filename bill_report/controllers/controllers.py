# -*- coding: utf-8 -*-
# from odoo import http


# class BillReport(http.Controller):
#     @http.route('/bill_report/bill_report', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/bill_report/bill_report/objects', auth='public')
#     def list(self, **kw):
#         return http.request.render('bill_report.listing', {
#             'root': '/bill_report/bill_report',
#             'objects': http.request.env['bill_report.bill_report'].search([]),
#         })

#     @http.route('/bill_report/bill_report/objects/<model("bill_report.bill_report"):obj>', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('bill_report.object', {
#             'object': obj
#         })
