# -*- coding: utf-8 -*-

from odoo import models, fields, api,_

class account_payment_ext(models.Model):
    _inherit = 'account.payment'
    payment_record = fields.Char(string='Payment Records')


class account_invoice_ext(models.Model):
    _inherit = 'account.invoice'