# -*- coding: utf-8 -*-

from odoo import models, fields, api

class ContactExtension(models.Model):
    _inherit = 'res.partner'


    @api.onchange('name')
    def change_contact_case(self):
        if self.name:
            self.name = str(self.name).title()