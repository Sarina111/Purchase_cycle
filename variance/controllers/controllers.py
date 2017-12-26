# -*- coding: utf-8 -*-
from odoo import http

# class Variance(http.Controller):
#     @http.route('/variance/variance/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/variance/variance/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('variance.listing', {
#             'root': '/variance/variance',
#             'objects': http.request.env['variance.variance'].search([]),
#         })

#     @http.route('/variance/variance/objects/<model("variance.variance"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('variance.object', {
#             'object': obj
#         })