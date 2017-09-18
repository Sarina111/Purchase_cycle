# -*- coding: utf-8 -*-

from odoo import models, fields, api, _
from odoo.exceptions import UserError, RedirectWarning, ValidationError
import requests
import odoo.addons.decimal_precision as dp
from datetime import datetime

class sales_ext_invoice(models.Model):
    _inherit = 'account.invoice'
    date_invoice = fields.Date(string='Invoice Date',
                               readonly=True, index=True,
                               help="Keep empty to use the current date", copy=False, default=fields.Datetime.now)
    sno = fields.Char(index=True,string='S.O No.')
    payment_type = fields.Selection(
        [('not_started', '--Select  Payment Type--'), ('cash', 'Cash'), ('cheque', 'Cheque'), ('credit', 'Credit'),
         ('others', 'Others')], default='not_started')

    # vehicle_no = fields.Many2one('loadingslip.loadingslip', required=True, string='Vehicle No')
    pan_num = fields.Char(string="PAN Number", related='partner_id.pan_number', store=True, size=9, readonly=True)
    # created_by = fields.Many2one('hr.employee', required=True, string='Bill Prepared By')
    fiscal_year = fields.Selection(
        [('not_started', '--Select Fiscal Year--'), ('0', '2072/2073'), ('1', '2073/2074'), ('2', '2074/2075'),
         ('3', '2075/2076')], default='not_started')

    vehicle_no = fields.Char(string='Vehicle No',
                             readonly=True)
    company = fields.Char( string="Transport Company")
    company_phone = fields.Char(string="Company Mobile")
    driver_name = fields.Char(string="Driver")
    mobile_driver = fields.Char(string='Phone')
    license = fields.Char(string='license')
    vehicle_type = fields.Char(string='Vehicle Number')
    dharma_no = fields.Char(string='Dharma No')
    driver_add = fields.Char(string='Driver Address')
    key_person = fields.Char(string='Key Person')
    team_id = fields.Many2one(help="Enter team's name", readonly=True)

    # driver_number = fields.Char(string='Driver name')


    # price_subtotal = fields.Monetary(string='Amount',store=True, readonly=True, compute='_compute_price')


    @api.multi
    def _create_bharpai(self):

        # pdb.set_trace()
        # pprint(self)
        recoo = []
        inv_obj = self.env['bharpai.bharpai']
        # i = -1
        for r in self:
            for re in r.invoice_line_ids:
                # i = i + 1
                recoo.append((0, 0, {'product_id': re.product_id.name,
                                     'quantity': re.quantity,
                                     'price_unit': re.price_unit,
                                     'discount': re.discount

                                     }))

        for rec in self:
            slip = inv_obj.create({
                'partner_id': rec.partner_id.name,
                'invoice_date': rec.date_invoice,
                # 'expiration_date': rec.validity_date,
                'si_no': rec.number,
                'truck_no':rec.vehicle_no,
                'company': rec.company,
                'driver_name': rec.driver_name,
                'invoice_line': recoo

            })
        return slip

    @api.multi
    def create_checklist(self):
        recoo = []
        inv_obj = self.env['checklist.dispatch']
        # i = -1
        for r in self:
            for re in r.invoice_line_ids:
                # i = i + 1
                recoo.append((0, 0, {'product_id': re.product_id.name,
                                     'quantity': re.quantity,

                                     }))
        for rec in self:
            slip = inv_obj.create({
                'partner_id': rec.partner_id.name,
                'invoice_date': rec.date_invoice,
                # 'expiration_date': rec.validity_date,
                'truck_no': rec.vehicle_no,
                'company': rec.company,
                'driver_name': rec.driver_name,
                'mobile_driver':rec.mobile_driver,
                'si_no': rec.number,
                'so_no':rec.origin,
                'dharma_no':rec.dharma_no,
                'customer_mobile': rec.partner_id.mobile,
                'sales_mobile': rec.user_id.mobile,
                'invoice_line_checklist': recoo
            })
            return slip




    @api.multi
    def bhada_chalan(self):

        # pdb.set_trace()
        # pprint(self)
        recoo = []
        inv_obj = self.env['bhada.chalan1']
        for r in self:
            for re in r.invoice_line_ids:
                # i = i + 1
                recoo.append((0, 0, {'product_id': re.product_id.name,
                                     'quantity': re.quantity,
                                     }))

        for rec in self:
            slip = inv_obj.create({
                'customer_name': rec.partner_id.name,
                'invoice_date': rec.date_invoice,
                'invoice_no': rec.number,
                'veh_no1': rec.vehicle_no,
                'company':rec.company,
                'company_phone':rec.company_phone,
                'driver_name':rec.driver_name,
                'mobile_driver':rec.mobile_driver,
                'driver_lic1':rec.license,
                'veh_type1':rec.vehicle_type,
                'driver_add' : rec.driver_add,
                'key_person' : rec.key_person,
                'dharma_no':rec.dharma_no,
                'invoice_line_bhada': recoo

                # 'expiration_date': rec.validity_date,

                # 'invoice_line_pass': recoo

            })
        return slip


##########################################################
    # @api.depends('invoice_line')
    # @api.multi
    # def _create_bharpai(self):
    #     inv_obj = self.env['bharpai.bharpai']
    #     # self.ensure_one()
    #     slip = inv_obj.create({
    #         'si_no': self.name,
    #         'partner_id': self.partner_id.name,
    #         'invoice_date': self.date_invoice,
    #         # 'truck_no': self.validity_date,
    #         # self.dharmakata_btn()
    #     })
    #     self._data_sql(self.name)
    #     return slip
    #
    # def _data_sql(self, si_no):
    #     self.env.cr.execute('INSERT INTO bharpai_product(product_id,quantity,bh_id)'
    #                         'SELECT account_invoice_line.name,account_invoice_line.quantity,bharpai_bharpai.id'
    #                         'FROM account_invoice,account_invoice_line,bharpai_bharpai'
    #                         'WHERE account_invoice.id=account_invoice_line.invoice_id'
    #                         'AND account_invoice.name=bharpai_bharpai.si_no;')
    #
    # @api.depends('invoice_line_pass')
    # @api.multi
    # def _create_gatepass(self):
    #     inv_obj = self.env['gate.pass']
    #     # self.ensure_one()
    #     slip = inv_obj.create({
    #         'si_no': self.name,
    #         'partner_id': self.partner_id.name,
    #         'invoice_date': self.date_invoice,
    #         # 'truck_no': self.validity_date,
    #         # self.dharmakata_btn()
    #     })
    #     self._data_sql1(self.name)
    #     return slip
    #
    # def _data_sql1(self, si_no):
    #     self.env.cr.execute('INSERT INTO gatepass_product(product_id,quantity,bh_id) '
    #                         'SELECT account_invoice_line.name,account_invoice_line.quantity,gate_pass.id'
    #                         'FROM account_invoice,account_invoice_line,gate_pass'
    #                         'WHERE account_invoice.id=account_invoice_line.invoice_id'
    #                         'AND account_invoice.name=gate_pass.si_no;')
    #
#############################################################

    @api.multi
    def action_invoice_open(self):
        # lots of duplicate calls to action_invoice_open, so we remove those already open
        to_open_invoices = self.filtered(lambda inv: inv.state != 'open')
        if to_open_invoices.filtered(lambda inv: inv.state not in ['proforma2', 'draft']):
            raise UserError(_("Invoice must be in draft or Pro-forma state in order to validate it."))
        to_open_invoices.action_date_assign()
        to_open_invoices.action_move_create()
        self.bhada_chalan()
        self._create_bharpai()
        self.create_checklist()
        # self._sms_trigger_invoice()
        return to_open_invoices.invoice_validate()

    def _sms_trigger_invoice(self):
        # sms_obj = self.env['sale.order']
        sms_obj1 = self.env['smsnp.send1']

        # for ss in self:
        send = sms_obj1.create({

            'text_to': self.partner_id.mobile,
            'create_uid': self.create_uid,
            'create_date': self.create_date,
            'text_msg': 'Dear Sir, Please confirm the Sale Order for the recently created quotation.',
            # 'text':
            'sale_name': self.number

        })
        send.write({'state': 'waiting_for_approval'})
        return send

    # @api.multi
    # def action_invoice_open(self):
    #     # lots of duplicate calls to action_invoice_open, so we remove those already open
    #     to_open_invoices = self.filtered(lambda inv: inv.state != 'open')
    #     if to_open_invoices.filtered(lambda inv: inv.state not in ['proforma2', 'draft']):
    #         raise UserError(_("Invoice must be in draft or Pro-forma state in order to validate it."))
    #     to_open_invoices.action_date_assign()
    #     to_open_invoices.action_move_create()
    #     self._create_bharpai()
    #     # self.create_gatepass()
    #     self.bhada_chalan()
    #     # self.post_msg_customer()
    #     self._create_gatepass()
    #     return to_open_invoices.invoice_validate()


    #
    # # send sms to customer
    # def post_msg_customer(self):
    #     # import pdb;
    #     # test.set_trace()
    #     # pprint('token')
    #     # pprint('text_from')
    #     # pprint('text_to')
    #     r = requests.get(
    #         "http://api.sparrowsms.com/v2/sms",
    #         params={
    #             'token': '4symSqCEVvG1zIEdWFcz',
    #             'from': 'InfoSMS',
    #             'to': self.user_id.mobile,
    #             # 'text': 'This text message is forwarded to / user_id.name / team_id for / partner_id '
    #             'text': 'Dear Customer,'
    #                     'Your invoice has been cleared.'
    #         }
    #     )
    #     return r


    amount_exc = fields.Monetary(string='Taxable Amount', readonly=True)
    amount_untaxed = fields.Monetary(string='Taxable Amount',
                                     store=True, readonly=True, compute='_compute_amount', track_visibility='always')
    amount_excise = fields.Monetary(string='Excise Duty', readonly=True,compute='_compute_amount')
    total_dis = fields.Monetary(string='Total Discount', readonly=True,store=True,compute='_compute_amount')
    amount_dis=fields.Monetary(string='Sub-Total',compute='_compute_amount')
    amount_tax = fields.Monetary(string='VAT',
                                 store=True, readonly=True, compute='_compute_amount')

    @api.one
    @api.depends('invoice_line_ids.price_subtotal', 'tax_line_ids.amount', 'currency_id', 'company_id', 'date_invoice',
                 'type')
    def _compute_amount(self):

        self.total_dis= sum(line.total_dis for line in self.invoice_line_ids)
        self.amount_dis=sum(line.price_subtotal for line in self.invoice_line_ids)- self.total_dis
        self.amount_excise=sum(line.quantity for line in self.invoice_line_ids)*9
        # self.amount_exc=self.amount_dis-self.amount_excise
        # self.amount_untaxed = sum(line.price_subtotal for line in self.invoice_line_ids)
        self.amount_untaxed=self.amount_dis+self.amount_excise
        self.amount_tax = sum(line.amount for line in self.tax_line_ids)



        self.amount_total = self.amount_untaxed + self.amount_tax
        amount_total_company_signed = self.amount_total
        amount_untaxed_signed = self.amount_untaxed
        if self.currency_id and self.company_id and self.currency_id != self.company_id.currency_id:
            currency_id = self.currency_id.with_context(date=self.date_invoice)
            amount_total_company_signed = currency_id.compute(self.amount_total, self.company_id.currency_id)
            amount_untaxed_signed = currency_id.compute(self.amount_untaxed, self.company_id.currency_id)
        sign = self.type in ['in_refund', 'out_refund'] and -1 or 1
        self.amount_total_company_signed = amount_total_company_signed * sign
        self.amount_total_signed = self.amount_total * sign
        self.amount_untaxed_signed = amount_untaxed_signed * sign

    @api.multi
    def get_taxes_values(self):
        tax_grouped = {}
        # price_unit = self.amount_untaxed
        for line in self.invoice_line_ids:
            # price_unit = line.price_unit * (1 - (line.discount or 0.0) / 100.0)
            price_unit=(line.price_unit- line.discount+9)

            taxes = line.invoice_line_tax_ids.compute_all(price_unit, self.currency_id, line.quantity, line.product_id, self.partner_id)['taxes']

            for tax in taxes:
                val = self._prepare_tax_line_vals(line, tax)
                key = self.env['account.tax'].browse(tax['id']).get_grouping_key(val)

                if key not in tax_grouped:
                    tax_grouped[key] = val
                else:
                    tax_grouped[key]['amount'] += val['amount']
                    tax_grouped[key]['base'] += val['base']
        return tax_grouped




class invoice_order_inherit(models.Model):
    _inherit='account.invoice.line'
    discount = fields.Float(string='Discount (Rs)', digits=dp.get_precision('Discount'),
                            default=0.0)
    total_dis=fields.Float(string='Price With Discount',compute='_compute_price')
    mrp=fields.Float(string='Mrp')

    @api.one
    @api.depends('price_unit', 'discount', 'invoice_line_tax_ids', 'quantity','total_dis',
                 'product_id', 'invoice_id.partner_id', 'invoice_id.currency_id', 'invoice_id.company_id',
                 'invoice_id.date_invoice')
    def _compute_price(self):
        currency = self.invoice_id and self.invoice_id.currency_id or None
        # price = self.price_unit * (1 - (self.discount or 0.0) / 100.0)
        price = self.price_unit
        self.total_dis=self.quantity*self.discount
        taxes = False
        if self.invoice_line_tax_ids:
            taxes = self.invoice_line_tax_ids.compute_all(price, currency, self.quantity, product=self.product_id,
                                                          partner=self.invoice_id.partner_id)
        self.price_subtotal = price_subtotal_signed = taxes['total_excluded'] if taxes else self.quantity * price

        if self.invoice_id.currency_id and self.invoice_id.company_id and self.invoice_id.currency_id != self.invoice_id.company_id.currency_id:
            price_subtotal_signed = self.invoice_id.currency_id.with_context(date=self.invoice_id.date_invoice).compute(
                price_subtotal_signed, self.invoice_id.company_id.currency_id)
        sign = self.invoice_id.type in ['in_refund', 'out_refund'] and -1 or 1
        self.price_subtotal_signed = price_subtotal_signed * sign



