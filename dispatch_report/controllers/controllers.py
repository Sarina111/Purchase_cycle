# -*- coding: utf-8 -*-
from odoo import http

# class BharpaiReport(http.Controller):
#     @http.route('/bharpai_report/bharpai_report/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/bharpai_report/bharpai_report/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('bharpai_report.listing', {
#             'root': '/bharpai_report/bharpai_report',
#             'objects': http.request.env['bharpai_report.bharpai_report'].search([]),
#         })

#     @http.route('/bharpai_report/bharpai_report/objects/<model("bharpai_report.bharpai_report"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('bharpai_report.object', {
#             'object': obj
#         })