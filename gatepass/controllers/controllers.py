# -*- coding: utf-8 -*-
from odoo import http

# class Gatepass/(http.Controller):
#     @http.route('/gatepass//gatepass//', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/gatepass//gatepass//objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('gatepass/.listing', {
#             'root': '/gatepass//gatepass/',
#             'objects': http.request.env['gatepass/.gatepass/'].search([]),
#         })

#     @http.route('/gatepass//gatepass//objects/<model("gatepass/.gatepass/"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('gatepass/.object', {
#             'object': obj
#         })