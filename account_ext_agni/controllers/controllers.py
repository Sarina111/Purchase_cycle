# -*- coding: utf-8 -*-
from odoo import http

# class AccountExtAgni(http.Controller):
#     @http.route('/account_ext_agni/account_ext_agni/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/account_ext_agni/account_ext_agni/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('account_ext_agni.listing', {
#             'root': '/account_ext_agni/account_ext_agni',
#             'objects': http.request.env['account_ext_agni.account_ext_agni'].search([]),
#         })

#     @http.route('/account_ext_agni/account_ext_agni/objects/<model("account_ext_agni.account_ext_agni"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('account_ext_agni.object', {
#             'object': obj
#         })