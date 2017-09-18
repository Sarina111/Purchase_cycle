# -*- coding: utf-8 -*-

from odoo import models, fields, api,_
import requests

class _gatepass(models.Model):
    _name = 'gate.pass'
    _description = 'gatepass information'
    partner_id = fields.Char("Customer")
    # partner_id = fields.Many2one('res.partner', string='Custo')
    mobile = fields.Char(string='Mobile')
    invoice_date = fields.Date("Invoice Date")
    # invoice_line = fields.One2many('account.invoice.line','invoice_line_ids', string="Invoice Lines")
    truck_no = fields.Char("Vehicle No.")
    company = fields.Char(string="Transport Company")

    driver_name = fields.Char("Driver")
    si_no = fields.Char("SI No.")

    invoice_line_pass = fields.One2many('gatepass.product', 'bh_id', 'Loading ID')
    name = fields.Char(
        'Loading_slip ID', copy=False, readonly=True, default=lambda x: _('New'))
    state = fields.Selection([('draft','SMS Pending'),('sent','SMS Sent')])


    @api.depends('mobile')
    def post_msg(self):
        # import pdb;
        # pdb.set_trace()
        # pprint('token')
        # pprint('text_from')
        # pprint('text_to')
        r = requests.get(
            "http://api.sparrowsms.com/v2/sms",
            params={
                'token': '4symSqCEVvG1zIEdWFcz',
                'from': 'InfoSMS',
                # 'to': self.user_id.mobile,
                # 'to': self.user_id.mobile,
                'to': self.mobile,
                # 'text': 'This is test message'
                'text': 'Dear Customer, Your order is in your way.'
            }
        )
        self.sms_trigger_gatepass()
        self.gatepass_state()
        return r

    def gatepass_state(self):
        self.write({'state': 'sent'})




    def sms_trigger_gatepass(self):
        # sms_obj = self.env['sale.order']
        sms_obj1 = self.env['smsnp.send1']

        # for ss in self:
        send = sms_obj1.create({

            'text_to': self.mobile,
            'create_uid': self.create_uid,
            'create_date': self.create_date,
            'text_msg': 'Dear Customer, Your order is in your way.'
            # 'text':

        })
        send.write({'state': 'approved'})
        return send

    # auto generation of serial number ###
    @api.model
    def create(self, valueees):
        if valueees.get('name', _('New')) == _('New'):
            valueees['name'] = self.env['ir.sequence'].next_by_code('gate.pass') or _('New')
        return super(_gatepass, self).create(valueees)

        # many to one relaiton with loading.slip ###


class product_tree(models.Model):
    _name = 'gatepass.product'
    _description = 'gatepass tree'
    bh_id = fields.Many2one('gate.pass', string='Bharpai ID')
    sno = fields.Char("S.No")
    product_id = fields.Char("Product", store=True)
    # invoice_line = fields.One2many('account.invoice.line','invoice_line_ids', string="Invoice Lines")
    quantity = fields.Char("Quantity", store=True)
    # total_qty = fields.Float("Total Quantity", compute="_compute_total", store=True, readonly=True)
    #
    # @api.depends('quantity')
    # def _compute_total(self):
    #     for line in self:
    #         line.total_qty += line.quantity