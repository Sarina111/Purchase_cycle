# -*- coding: utf-8 -*-
from odoo import http

# class PragyapanPatra(http.Controller):
#     @http.route('/pragyapan_patra/pragyapan_patra/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/pragyapan_patra/pragyapan_patra/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('pragyapan_patra.listing', {
#             'root': '/pragyapan_patra/pragyapan_patra',
#             'objects': http.request.env['pragyapan_patra.pragyapan_patra'].search([]),
#         })

#     @http.route('/pragyapan_patra/pragyapan_patra/objects/<model("pragyapan_patra.pragyapan_patra"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('pragyapan_patra.object', {
#             'object': obj
#         })