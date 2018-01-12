# -*- coding: utf-8 -*-

from odoo import models, fields, api,_
import webbrowser
#

# class account_inherit(models.Model):
#     inherit = 'account.invoice'
#     pan_num = fields.Char(string='Pan number')

    # data mapping ###
    # left side sales.registerko field
    # @api.multi
    # def create_register(self):
    #     inv_obj = self.env['sales.register']
    #     self.ensure_one()
    #     slip = inv_obj.create({
    #         'name': self.partner_id,
    #         'invoice_date': self.date_invoice,
    #         'invoice_number': self.name,
    #         # '': self.name,
    #     })
    #     return slip
    #
    # def create_register_btn(self):
    #     self._create_register()



class account_ext(models.Model):
    _name='account.ase'

    def open1(self):
        webbrowser.open_new(r'account_ext/models/user_manual_accounting.pdf')
    #
    # def generate_xml(self, cr, uid, ids, context=None):
    #     xml_data = text_to_write_in_xml
    #     file = base64.encodestring(xml_data)
    #     self.write(cr, uid, ids, {'filedata': file, 'name': "file.xml"}, context=context)
    #     return {
    #         'type': 'ir.actions.act_window',
    #         'res_model': 'my.class',
    #         'view_mode': 'form',
    #         'view_type': 'form',
    #         'target': ids,
    #         'context': dict(context, active_ids=ids)
    #         'views': [(False, 'form')],
    #         'target': 'new',
    #     }

class invoice_inherit(models.Model):
    _inherit = 'account.invoice'
    untaxed_amount = fields.Float("Total Untaxed", compute="_compute_untaxed", store=True, readonly=True)

    @api.depends('amount_untaxed')
    def _compute_untaxed(self):
        for line in self:
            line.untaxed_amount += line.amount_untaxed



    # pan_number = fields.Char(string='PAN Number',related='partner_id.pan_number')

# class sales_register(models.Model):
#     _name = 'sales.register'
#     _inherit = ['account.invoice']
#     # account_id = fields.Many2one('account.invoice')
#
#     # invoice_date = fields.Date(string='Invoice Date')
#     # name = fields.Many2one('res.partner',string='Customer')
#     pan_number = fields.Char(string='PAN Number')
#     # data mapping ###
    # left side sales.registerko field
    # @api.multi
    # def create_register(self):
    #     inv_obj = self.env['sales.register']
    #     self.ensure_one()
    #     slip = inv_obj.create({
    #         'name': self.partner_id,
    #         'invoice_date': self.date_invoice,
    #         'invoice_number': self.name,
    #         # '': self.name,
    #     })
    #     return slip
    #
    # def create_register_btn(self):
    #     self._create_register()

    # invoice_number = fields.Char(sting='Invoice number')
    # total = fields.Char(string='Total sales')
    # amt_without_vat = fields.Char(string='amount without tax')
    # unit_price = fields.Char(string='Unit Price')


# class purchases_register(models.Model):
#     _name = 'purchases.register'
#     _inherit = ['account.invoice']



# |approver in payment
class payment_extended(models.Model):
     _inherit="account.payment"
     approver=fields.Many2one('res.user',string='Approver')
     