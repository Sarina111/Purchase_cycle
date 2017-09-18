# -*- coding: utf-8 -*-
from odoo import http

# class Proforma(http.Controller):
#     @http.route('/proforma/proforma/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/proforma/proforma/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('proforma.listing', {
#             'root': '/proforma/proforma',
#             'objects': http.request.env['proforma.proforma'].search([]),
#         })

#     @http.route('/proforma/proforma/objects/<model("proforma.proforma"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('proforma.object', {
#             'object': obj
#         })