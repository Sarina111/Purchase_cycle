# -*- coding: utf-8 -*-
from odoo import http

# class SalesExtAgni(http.Controller):
#     @http.route('/sales_ext_agni/sales_ext_agni/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/sales_ext_agni/sales_ext_agni/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('sales_ext_agni.listing', {
#             'root': '/sales_ext_agni/sales_ext_agni',
#             'objects': http.request.env['sales_ext_agni.sales_ext_agni'].search([]),
#         })

#     @http.route('/sales_ext_agni/sales_ext_agni/objects/<model("sales_ext_agni.sales_ext_agni"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('sales_ext_agni.object', {
#             'object': obj
#         })