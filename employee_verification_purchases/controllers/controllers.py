# -*- coding: utf-8 -*-
# from odoo import http


# class EmployeeVerificationPurchases(http.Controller):
#     @http.route('/employee_verification_purchases/employee_verification_purchases', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/employee_verification_purchases/employee_verification_purchases/objects', auth='public')
#     def list(self, **kw):
#         return http.request.render('employee_verification_purchases.listing', {
#             'root': '/employee_verification_purchases/employee_verification_purchases',
#             'objects': http.request.env['employee_verification_purchases.employee_verification_purchases'].search([]),
#         })

#     @http.route('/employee_verification_purchases/employee_verification_purchases/objects/<model("employee_verification_purchases.employee_verification_purchases"):obj>', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('employee_verification_purchases.object', {
#             'object': obj
#         })
