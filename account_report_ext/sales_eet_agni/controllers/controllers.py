# -*- coding: utf-8 -*-
from odoo import http

# class SalesEetAgni(http.Controller):
#     @http.route('/sales_eet_agni/sales_eet_agni/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/sales_eet_agni/sales_eet_agni/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('sales_eet_agni.listing', {
#             'root': '/sales_eet_agni/sales_eet_agni',
#             'objects': http.request.env['sales_eet_agni.sales_eet_agni'].search([]),
#         })

#     @http.route('/sales_eet_agni/sales_eet_agni/objects/<model("sales_eet_agni.sales_eet_agni"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('sales_eet_agni.object', {
#             'object': obj
#         })