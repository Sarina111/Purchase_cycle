# -*- coding: utf-8 -*-
from odoo import http

# class ResPartnerExt(http.Controller):
#     @http.route('/res_partner_ext/res_partner_ext/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/res_partner_ext/res_partner_ext/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('res_partner_ext.listing', {
#             'root': '/res_partner_ext/res_partner_ext',
#             'objects': http.request.env['res_partner_ext.res_partner_ext'].search([]),
#         })

#     @http.route('/res_partner_ext/res_partner_ext/objects/<model("res_partner_ext.res_partner_ext"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('res_partner_ext.object', {
#             'object': obj
#         })