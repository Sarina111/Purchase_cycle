# -*- coding: utf-8 -*-
from odoo import http

# class Odoo-template(http.Controller):
#     @http.route('/odoo-template/odoo-template/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/odoo-template/odoo-template/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('odoo-template.listing', {
#             'root': '/odoo-template/odoo-template',
#             'objects': http.request.env['odoo-template.odoo-template'].search([]),
#         })

#     @http.route('/odoo-template/odoo-template/objects/<model("odoo-template.odoo-template"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('odoo-template.object', {
#             'object': obj
#         })