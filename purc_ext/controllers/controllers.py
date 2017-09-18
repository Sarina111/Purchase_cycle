# -*- coding: utf-8 -*-
from odoo import http

# class Loadingslip(http.Controller):
#     @http.route('/loadingslip/loadingslip/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/loadingslip/loadingslip/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('loadingslip.listing', {
#             'root': '/loadingslip/loadingslip',
#             'objects': http.request.env['loadingslip.loadingslip'].search([]),
#         })

#     @http.route('/loadingslip/loadingslip/objects/<model("loadingslip.loadingslip"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('loadingslip.object', {
#             'object': obj
#         })