# -*- coding: utf-8 -*-
from odoo import http

# class AccountReportExt(http.Controller):
#     @http.route('/account_report_ext/account_report_ext/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/account_report_ext/account_report_ext/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('account_report_ext.listing', {
#             'root': '/account_report_ext/account_report_ext',
#             'objects': http.request.env['account_report_ext.account_report_ext'].search([]),
#         })

#     @http.route('/account_report_ext/account_report_ext/objects/<model("account_report_ext.account_report_ext"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('account_report_ext.object', {
#             'object': obj
#         })