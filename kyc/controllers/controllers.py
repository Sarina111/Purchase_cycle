# -*- coding: utf-8 -*-
from odoo import http

# class Kyc(http.Controller):
#     @http.route('/kyc/kyc/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/kyc/kyc/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('kyc.listing', {
#             'root': '/kyc/kyc',
#             'objects': http.request.env['kyc.kyc'].search([]),
#         })

#     @http.route('/kyc/kyc/objects/<model("kyc.kyc"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('kyc.object', {
#             'object': obj
#         })