# -*- coding: utf-8 -*-
from odoo import http

# class Bharpai(http.Controller):
#     @http.route('/bharpai/bharpai/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/bharpai/bharpai/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('bharpai.listing', {
#             'root': '/bharpai/bharpai',
#             'objects': http.request.env['bharpai.bharpai'].search([]),
#         })

#     @http.route('/bharpai/bharpai/objects/<model("bharpai.bharpai"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('bharpai.object', {
#             'object': obj
#         })