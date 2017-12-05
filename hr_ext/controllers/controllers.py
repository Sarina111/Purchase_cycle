# -*- coding: utf-8 -*-
from odoo import http

# class HrExt(http.Controller):
#     @http.route('/hr_ext/hr_ext/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/hr_ext/hr_ext/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('hr_ext.listing', {
#             'root': '/hr_ext/hr_ext',
#             'objects': http.request.env['hr_ext.hr_ext'].search([]),
#         })

#     @http.route('/hr_ext/hr_ext/objects/<model("hr_ext.hr_ext"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('hr_ext.object', {
#             'object': obj
#         })