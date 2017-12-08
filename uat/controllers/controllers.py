# -*- coding: utf-8 -*-
from odoo import http

# class Uat(http.Controller):
#     @http.route('/uat/uat/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/uat/uat/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('uat.listing', {
#             'root': '/uat/uat',
#             'objects': http.request.env['uat.uat'].search([]),
#         })

#     @http.route('/uat/uat/objects/<model("uat.uat"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('uat.object', {
#             'object': obj
#         })