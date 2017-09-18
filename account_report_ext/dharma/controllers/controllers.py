# -*- coding: utf-8 -*-
from odoo import http

# class Dharmakata(http.Controller):
#     @http.route('/dharmakata/dharmakata/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/dharmakata/dharmakata/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('dharmakata.listing', {
#             'root': '/dharmakata/dharmakata',
#             'objects': http.request.env['dharmakata.dharmakata'].search([]),
#         })

#     @http.route('/dharmakata/dharmakata/objects/<model("dharmakata.dharmakata"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('dharmakata.object', {
#             'object': obj
#         })