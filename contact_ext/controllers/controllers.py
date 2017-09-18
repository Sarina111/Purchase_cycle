# -*- coding: utf-8 -*-
from odoo import http

# class ContactExt(http.Controller):
#     @http.route('/contact_ext/contact_ext/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/contact_ext/contact_ext/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('contact_ext.listing', {
#             'root': '/contact_ext/contact_ext',
#             'objects': http.request.env['contact_ext.contact_ext'].search([]),
#         })

#     @http.route('/contact_ext/contact_ext/objects/<model("contact_ext.contact_ext"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('contact_ext.object', {
#             'object': obj
#         })