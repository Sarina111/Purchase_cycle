# -*- coding: utf-8 -*-
from odoo import http

# class SalesExtInvoice(http.Controller):
#     @http.route('/sales_ext_invoice/sales_ext_invoice/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/sales_ext_invoice/sales_ext_invoice/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('sales_ext_invoice.listing', {
#             'root': '/sales_ext_invoice/sales_ext_invoice',
#             'objects': http.request.env['sales_ext_invoice.sales_ext_invoice'].search([]),
#         })

#     @http.route('/sales_ext_invoice/sales_ext_invoice/objects/<model("sales_ext_invoice.sales_ext_invoice"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('sales_ext_invoice.object', {
#             'object': obj
#         })