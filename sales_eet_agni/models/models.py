# -*- coding: utf-8 -*-

from odoo import models, fields, api,_
from pprint import pprint
import pdb
import odoo.addons.decimal_precision as dp
from odoo.exceptions import UserError
from odoo.tools import float_is_zero, float_compare, DEFAULT_SERVER_DATETIME_FORMAT
import requests

from openerp.tools import DEFAULT_SERVER_DATE_FORMAT
from openerp.exceptions import Warning
from odoo.exceptions import ValidationError
from datetime import datetime,date
import dateutil.parser



from datetime import time

class sale_customer(models.Model):
    _inherit = 'res.partner'
    pan_selection = fields.Selection([('pan', 'Pan Number'), ('vat', 'VAT Number')],default='pan', string='Registration Type', required='True')
    pan_number = fields.Char(string='Registration Number', size=9, required='True')
    # vat_number = fields.Char(string='VAT Number')
    # bank_name = fields.Char(string='Bank Name')
    # acc_number = fields.Char(string='Account Number')
    p = fields.Selection(
        [('yes', 'Yes'), ('no', 'No')],
        default='no', string='Verification Status', required='True')
    contrat_start = fields.Date(string='Contract start Date')
    contract_status = fields.Selection(
        [('yes', 'Yes'), ('no', 'No')],
        default='no', string='Contract Status')
    key_person = fields.Char(string='Key Person')

    mobile_no=fields.Char(string='Mobile Number')
    license = fields.Char(string='license')
    mobile = fields.Char(required='True')
    region=fields.Selection(
        [('bhairawa', 'Bhairahawa'), ('ktm', 'Kathmandu')],
        default='bhairawa', string='Region', required='True')
    # payment_term_id = fields.Many2one('account.payment.term', string='Payment Terms')

    # payment_term = fields.Char( string='Payment Terms')




    # @api.constrains('pan_number')
    # def _validate(self):
    #     for pan in self:
    #         if len(pan.pan_number) < 8:
    #         raise ValidationError("Make sure your password is at least 8 letters")
    #     elif re.search('[0-9]',pan.pan_number) is None:
    #         raise ValidationError("Make sure your password has a number in it")
    #         elif re.search('[A-Z]',pan.pan_number) is None:
    #         raise ValidationError("Make sure your password has a capital letter in it")
    #
    #

# Inheriting sale order####

class sale_func(models.Model):
    _inherit = 'sale.order'

    address = fields.Char(string='Address',related='partner_id.street')

    typo=fields.Selection(
        [ ('done', 'Done'), ('no', 'No')],
        string='Loading Status')
    state = fields.Selection([
        ('draft', 'Order Estimation'),
        ('sent', 'Order Estimation Sent'),
        ('sale', 'Sales Order'),
        ('done', 'Locked'),
        ('cancel', 'Cancelled'),
    ], string='Status', readonly=True, copy=False, index=True, track_visibility='onchange', default='draft')

    amount_untaxed = fields.Monetary(string='Sub-Total', store=True, readonly=True, compute='_amount_all',
                                     track_visibility='always')
    date_order = fields.Datetime(string='Order Date', required=True, readonly=True, default=fields.Datetime.now)


    com = fields.Char(string="Transport Company",translate=True)
    company_phone=fields.Char(string="Company Mobile")


    driver_name = fields.Char("Driver")
    truck_no = fields.Char(string='Truck_no')
    license=fields.Char(string="License")

    vehicle_type = fields.Char(string='Vehicle Type')

    mobile_driver = fields.Char(string='Phone')
    driver_add = fields.Char(string='Driver Address')
    key_person = fields.Char(string='Key person')

    amount_exc=fields.Monetary(string='Taxable Amount',readonly=True, store=True,track_visibility='always',compute='_amount_all',)
    amount_excise = fields.Monetary(string='Excise Duty',readonly=True, store=True,track_visibility='always',compute='_amount_all',)
    total_dis=fields.Monetary(string='Total Discount',readonly=True, store=True,track_visibility='always',compute='_amount_all',)
    count_record=fields.Float(string="Count Record",default='1.0')
    delivery_mobile=fields.Char(string='Delivery phone',related='partner_shipping_id.mobile')

    dharma_no = fields.Char(string='Dharma No')
    amount_tax = fields.Monetary(string='VAT', store=True, readonly=True, compute='_amount_all', track_visibility='always')


    # @api.constrains('validity_date')
    # def datevalidation(self):
    #     for datee in self:
    #         if self.validity_date <= self.date_order:
    #             raise ValidationError("Expiration Date should always be later than Ordered Date")


    # count_r=fields.Integer(compute='c_record')

    # @api.depends('count_record')
    # def c_record(self):
    #
    #     count=0.0
    #     for order in self:
    #             for line in order:
    #         # for line in order.bh_id1:
    #                 count+= line.count_record
    #
    #     order.update({
    #         'count_r': count
    #     })
    #     self.count_count()

    validity_date = fields.Datetime(string='Expiration Date', readonly=True,
                                                                help="Manually set the expiration date of your quotation (offer), or it will set the date automatically based on the template if online quotation is installed.")

    # @api.depends('date_order')
    # @api.constrains('validity_date')
    # def onchange_date(self):
    #     # v_date=end_date=False
    #     # for order in self:
    #     if self.validity_date:
    #             # v_date=datetime.strptime(self.date_order, DEFAULT_SERVER_DATE_FORMAT).date()
    #         if datetime.strftime(self.validity_date, DEFAULT_SERVER_DATE_FORMAT).date() < datetime.now().date():
    #             raise ValidationError('Please select a date equal/or greater than the current date')
    #             return False
    #         else:
    #             return self.validity_date[:self.validity_date.rindex(" ")+5]
            # end_date = v_date + datetime.timedelta(days=10)


    @api.onchange('partner_id')
    def addDate(self):
        # test.set_trace()
        # if self.validity_date:
        d = date.today()
        # pprint(d)
        tdate = date(d.year, d.month, d.day)
        tdate = tdate.replace(day=d.day + 3)
        add_date = tdate.strftime(DEFAULT_SERVER_DATE_FORMAT)
        # pprint(add_date)
        self.validity_date = add_date
        # raise ValidationError('Error')

    @api.one
    def count_count(self):
        count_list = self.env['crm.team']
        count_list.write(
        {
            'count':self.count_record
        })


    ##############################################

    # @api.depends('invoice_line_ids')
    # @api.multi
    # def _create_slip(self):
    #     inv_obj = self.env['loading.slip']
    #     # self.ensure_one()
    #     slip = inv_obj.create({
    #         'so_no': self.name,
    #         'partner_id': self.partner_id.name,
    #         'order_date': self.date_order,
    #         'expiration_date': self.validity_date,
    #         # self.dharmakata_btn()
    #     })
    #     self._data_sql(self.name)
    #     return slip
    #
    # def _data_sql(self, so_no):
    #     self.env.cr.execute('INSERT INTO loading_product(product_id,quantity,bh_id) '
    #                         'SELECT sale_order_line.name,sale_order_line.product_uom_qty,loading_slip.id'
    #                         ' FROM sale_order,sale_order_line,loading_slip '
    #                         'WHERE sale_order.id=sale_order_line.order_id '
    #                         'AND sale_order.name=loading_slip.so_no;')
    #
    # @api.multi
    # def action_confirm(self):
    #     for order in self:
    #         order.state = 'sale'
    #         order.confirmation_date = fields.Datetime.now()
    #         if self.env.context.get('send_email'):
    #             self.force_quotation_send()
    #             order.order_line._action_procurement_create()
    #         if self.env['ir.values'].get_default('sale.config.settings', 'auto_done_setting'):
    #             self.action_done()
    #         self._create_slip()
    #         # self._create_product()
    #         # self._create_dk()
    #         # self.tab()
    #         return True

###################################################

    # create invoice method####

    @api.multi
    def action_invoice_create(self, grouped=False, final=False):
        """
        Create the invoice associated to the SO.
        :param grouped: if True, invoices are grouped by SO id. If False, invoices are grouped by
                        (partner_invoice_id, currency)
        :param final: if True, refunds will be generated if necessary
        :returns: list of created invoices
        """
        inv_obj = self.env['account.invoice']
        precision = self.env['decimal.precision'].precision_get('Product Unit of Measure')
        invoices = {}
        references = {}
        for order in self:
            group_key = order.id if grouped else (order.partner_invoice_id.id, order.currency_id.id)
            for line in order.order_line.sorted(key=lambda l: l.qty_to_invoice < 0):
                if float_is_zero(line.qty_to_invoice, precision_digits=precision):
                    continue
                if group_key not in invoices:
                    inv_data = order._prepare_invoice()
                    invoice = inv_obj.create(inv_data)
                    references[invoice] = order
                    invoices[group_key] = invoice
                elif group_key in invoices:
                    vals = {}
                    if order.name not in invoices[group_key].origin.split(', '):
                        vals['origin'] = invoices[group_key].origin + ', ' + order.name
                    if order.client_order_ref and order.client_order_ref not in invoices[group_key].name.split(
                            ', ') and order.client_order_ref != invoices[group_key].name:
                        vals['name'] = invoices[group_key].name + ', ' + order.client_order_ref
                    invoices[group_key].write(vals)
                if line.qty_to_invoice > 0:
                    line.invoice_line_create(invoices[group_key].id, line.qty_to_invoice)
                elif line.qty_to_invoice < 0 and final:
                    line.invoice_line_create(invoices[group_key].id, line.qty_to_invoice)

            if references.get(invoices.get(group_key)):
                if order not in references[invoices[group_key]]:
                    references[invoice] = references[invoice] | order

        if not invoices:
            raise UserError(_('There is no invoicable line.'))

        for invoice in invoices.values():
            if not invoice.invoice_line_ids:
                raise UserError(_('There is no invoicable line.'))
            # If invoice is negative, do a refund invoice instead
            if invoice.amount_untaxed < 0:
                invoice.type = 'out_refund'
                for line in invoice.invoice_line_ids:
                    line.quantity = -line.quantity
            # Use additional field helper function (for account extensions)
            for line in invoice.invoice_line_ids:
                line._set_additional_fields(invoice)
            # Necessary to force computation of taxes. In account_invoice, they are triggered
            # by onchanges, which are not triggered when doing a create.
            invoice.compute_taxes()
            invoice.message_post_with_view('mail.message_origin_link',
                                           values={'self': invoice, 'origin': references[invoice]},
                                           subtype_id=self.env.ref('mail.mt_note').id)
        # self._create_slip()
        # self._create_kata()
        self.update_inv1()
        return [inv.id for inv in invoices.values()]


        ########################################################
                # # data mapping1 ###
    @api.multi
    def _create_slip(self):
        #
        # pdb.set_trace()
        # pprint(self)
        recoo = []
        inv_obj = self.env['loading.slip']
        # i = -1
        for r in self:
            for re in r.order_line:
                # i = i + 1
                recoo.append((0,0,{'product_id': re.product_id.name,
                                   'quantity': re.product_uom_qty,
                                   }))


        for rec in self:
            slip = inv_obj.create({
                'partner_id': rec.partner_id.name,
                'order_date': rec.date_order,
                'expiration_date': rec.validity_date,
                'so_no': rec.name,
                'invoice_line_ids':recoo
            })
        slip.write({'state':'draft'})
        return slip



    ####################################

    def update_inv1(self):
        self.ensure_one()
        rec = self.env['account.invoice'].search([('origin', '=', self.name)])
        if rec:
            rec.vehicle_no = self.truck_no
            rec.company = self.com
            rec.company_phone = self.company_phone
            rec.driver_name = self.driver_name
            rec.mobile_driver = self.mobile_driver
            rec.license = self.license
            rec.vehicle_type = self.vehicle_type
            rec.dharma_no=self.dharma_no
            rec.driver_add = self.driver_add
            rec.key_person = self.key_person







    ######################################################

    def _sms_trigger(self):

        # sms_obj = self.env['sale.order']
        sms_obj1 = self.env['smsnp.send1']

        # for ss in self:
        send = sms_obj1.create({

            # 'text_to': self.partner_id.mobile,
            'text_to': self.partner_id.mobile,
            'create_uid': self.create_uid,

            'create_date': self.create_date,
            'text_msg': 'Dear Sir, Please confirm the Sale Order for the recently created quotation.',
            # 'text':
            'sale_name': self.name

        })
        send.write({'state': 'waiting_for_approval'})
        return send

        #############################################
    #slae order confirmation method#####
    @api.multi
    def action_confirm(self):
        for order in self:
            order.state = 'sale'
            order.confirmation_date = fields.Datetime.now()
            if self.env.context.get('send_email'):
                self.force_quotation_send()
                order.order_line._action_procurement_create()
            if self.env['ir.values'].get_default('sale.config.settings', 'auto_done_setting'):
                self.action_done()
            self._create_slip()
            # self._sms_trigger()
            # self.post_msg_manager()
            # self._create_kata()
            # self._create_dk()
            # self.tab()
            return True

    def post_msg_manager(self):
        # import pdb;
        # test.set_trace()
        # pprint('token')
        # pprint('text_from')
        # pprint('text_to')
        r = requests.get(
            "http://api.sparrowsms.com/v2/sms",
            params={
                'token': '4symSqCEVvG1zIEdWFcz',
                'from': 'InfoSMS',
                'to': self.user_id.mobile,
                # 'text': 'This text message is forwarded to / user_id.name / team_id for / partner_id '
                'text': 'Dear Manager,'
                        'Sales order has been conformed.'
            }
        )
        return r


        ####################################
    @api.depends('order_line.price_total')
    def _amount_all(self):
        """
        Compute the total amounts of the SO.
        """
        for order in self:
            amount_untaxed = amount_tax=amount_excise =total_qty=amount_untaxed1=total_disc= amount_exc = 0.0
            for line in order.order_line:
                amount_untaxed += line.price_subtotal
                total_qty+=line.product_uom_qty
                # total_disc+=line.product_uom_qty*line.discount #### for mannual discount
                total_disc+=line.total_dis

                # FORWARDPORT UP TO 10.0
                if order.company_id.tax_calculation_rounding_method == 'round_globally':
                    price = line.price_unit * (1 - (line.discount or 0.0) / 100.0)
                    taxes = line.tax_id.compute_all(price, line.order_id.currency_id, line.product_uom_qty,
                                                    product=line.product_id, partner=order.partner_shipping_id)
                    amount_untaxed1 = amount_untaxed - total_disc
                    amount_excise = total_qty * 9
                    amount_exc=amount_untaxed1 +amount_excise

                    amount_tax += sum(t.get('amount_exc', 0.0) for t in taxes.get('taxes', []))
                    # amount_tax=amount_excise*0.13
                    total_dis = total_disc


                else:
                    amount_untaxed1=amount_untaxed-total_disc


                    # amount_tax += line.price_tax
                    amount_excise = total_qty * 9
                    amount_exc = amount_untaxed1 + amount_excise
                    amount_tax = amount_exc * 0.13
                    total_dis = total_disc

            order.update({
                'total_dis':order.pricelist_id.currency_id.round(total_disc),
                'amount_untaxed': order.pricelist_id.currency_id.round(amount_untaxed1),

                'amount_excise': order.pricelist_id.currency_id.round(amount_excise),
                'amount_exc': order.pricelist_id.currency_id.round(amount_exc),

                'amount_tax': order.pricelist_id.currency_id.round(amount_tax),
                'amount_total': amount_exc+amount_tax,
            })
    ########################################################

    # def update_inv(self):
    #     self.ensure_one()
    #     # rec = self.env['account.invoice'].search([('origin', '=', self.name)])
    #     for rec in self:
    #         rec.vehicle_no = self.truck_no



#############################################################
            #create invoice method##

class SaleAdvancePaymentInv_Ext(models.TransientModel):
    _inherit = "sale.advance.payment.inv"
    _description = "Sales Advance Payment Invoice"

    @api.multi
    def create_invoices(self):
        sale_orders = self.env['sale.order'].browse(self._context.get('active_ids', []))

        if self.advance_payment_method == 'delivered':
            sale_orders.action_invoice_create()
        elif self.advance_payment_method == 'all':
            sale_orders.action_invoice_create(final=True)
        else:
            # Create deposit product if necessary
            if not self.product_id:
                vals = self._prepare_deposit_product()
                self.product_id = self.env['product.product'].create(vals)
                self.env['ir.values'].sudo().set_default('sale.config.settings', 'deposit_product_id_setting',
                                                         self.product_id.id)

            sale_line_obj = self.env['sale.order.line']
            for order in sale_orders:
                if self.advance_payment_method == 'percentage':
                    amount = order.amount_untaxed * self.amount / 100
                else:
                    amount = self.amount
                if self.product_id.invoice_policy != 'order':
                    raise UserError(_(
                        'The product used to invoice a down payment should have an invoice policy set to "Ordered quantities". Please update your deposit product to be able to create a deposit invoice.'))
                if self.product_id.type != 'service':
                    raise UserError(_(
                        "The product used to invoice a down payment should be of type 'Service'. Please use another product or update this product."))
                if order.fiscal_position_id and self.product_id.taxes_id:
                    tax_ids = order.fiscal_position_id.map_tax(self.product_id.taxes_id).ids
                else:
                    tax_ids = self.product_id.taxes_id.ids
                so_line = sale_line_obj.create({
                    'name': _('Advance: %s') % (time.strftime('%m %Y'),),
                    'price_unit': amount,
                    'product_uom_qty': 0.0,
                    'order_id': order.id,
                    'discount': 0.0,
                    'product_uom': self.product_id.uom_id.id,
                    'product_id': self.product_id.id,
                    'tax_id': [(6, 0, tax_ids)],
                })
                self._create_invoice(order, so_line, amount)
        if self._context.get('open_invoices', False):
            return sale_orders.action_view_invoice()

        # self.env["sale.order"]._create_slip()
        # self._create_kata()
        return {'type': 'ir.actions.act_window_close'}


######################################################################################################

class SaleOrderFunc(models.Model):
    _inherit = 'sale.order.line'
    price_subtotal = fields.Monetary(compute='_compute_amount', string='Subtotal', readonly=True, store=True)
    price_reduce = fields.Monetary(compute='_get_price_reduce', string='Price Reduce', readonly=True, store=True)
    total_dis=fields.Monetary(compute='_compute_amount')
    mrp=fields.Float(string='MRP')
    # price_unit = fields.Float('Unit Price',compute='mrp_product', required=True, digits=dp.get_precision('Product Price'), default=0.0)
    price_unit = fields.Float('Unit Price', required=True, default=0.0)
    discount = fields.Float(string='Discount (Rs.)',)


    # # @api.onchange('discount')
    # @api.depends('mrp','discount','price_unit')
    # def compute_unit(self):
    #     for line in self:
    #         # import pdb; pdb.set_trace()
    #         # pdb.set_trace()
    #         # pprint(self)
    #         # price=line.mrp - line.discount
    #
    #         # price=(((line.mrp-line.discount)/1.13)-9)+line.discount
    #         # price2= price-9+line.discount
    #         line.price_unit = line.mrp - line.discount
    #         return line.price_unit
    #         # line.price_unit = line.mrp - line.discount

    @api.onchange('product_id')
    def mrp_product(self):
        if self.product_id:
            self.mrp = self.product_id.mrp
            self.price_unit=self.product_id.list_price

    @api.depends('product_uom_qty','discount', 'price_unit', 'tax_id')
    def _compute_amount(self):
        for line in self:
            # price = line.price_unit - line.discount
            # price_unit=((line.mrp-line.discount)-1.13)-9+line.discount
            # line.price_unit=line.mrp-line.discount
            # dis=line.discount
            # line.price_unit=line.mrp-dis

            price = line.price_unit
            line.total_dis=line.discount*line.product_uom_qty
            taxes = line.tax_id.compute_all(price, line.order_id.currency_id, line.product_uom_qty, product=line.product_id,
                                            partner=line.order_id.partner_shipping_id)
            line.update({
                'price_tax': taxes['total_included'] - taxes['total_excluded'],
                'price_total': taxes['total_included'],
                'price_subtotal': taxes['total_excluded'],
             })

    # @api.onchange('discount')
    @api.depends('price_unit', 'discount')
    def _get_price_reduce(self):
        for line in self:
            # line.price_reduce = line.price_unit - line.discount
            # line.price_unit=line.mrp-line.discount
            line.price_reduce = line.price_unit

    @api.onchange('product_id','mrp','discount', 'price_unit', 'product_uom', 'product_uom_qty', 'tax_id')
    def _onchange_discount(self):
        # self.discount = 0.0
        if not (self.product_id and self.product_uom and
                    self.order_id.partner_id and self.order_id.pricelist_id and
                        self.order_id.pricelist_id.discount_policy == 'without_discount' and
                    self.env.user.has_group('sale.group_discount_per_so_line')):

            price_d=self.mrp-self.discount
            self.price_unit=(price_d/1.13)-9+25

    # discount = fields.Float(string='Discount (Rs.)', digits=dp.get_precision('Discount'), default=40.0)

#################################################################################################################################

class crm_inherit(models.Model):
    _inherit='crm.team'
    count=fields.Float(string='Count Record',)

    quotation = fields.Float(compute='quotation_count')
    sale_order = fields.Float(compute='sale_count')
    sent = fields.Float(compute='sent_count')
    locked = fields.Float(compute='done')
    cancel = fields.Float(compute='cancel_count')

    all = fields.Float(compute='all_count')

    quotation_fil = fields.Integer( compute='_compute_quotation')
    sale_orde_filr = fields.Integer(compute='_compute_sale')
    sent_fil = fields.Integer(compute='_compute_sent')
    locked_fil = fields.Integer(compute='_compute_locked')
    cancel_fil = fields.Integer(compute='_compute_cancel')



    @api.one
    def quotation_count(self):
        count_list = self.env['sale.order'].search_count([('state', '=', 'draft')])
        # count = len(count_list)
        self.quotation = count_list

    @api.one
    def sale_count(self):
        count = self.env['sale.order'].search_count([('state', '=', 'sale')])
        self.sale_order = count

    @api.one
    def sent_count(self):
        count = self.env['sale.order'].search_count([('state', '=', 'sent')])
        self.sent = count

    @api.one
    def done(self):
        count = self.env['sale.order'].search_count([('state', '=', 'done')])
        self.locked = count

    @api.one
    def cancel_count(self):
        count = self.env['sale.order'].search_count([('state', '=', 'cancel')])
        self.cancel= count

    @api.one
    def all_count(self):
        self.all = self.quotation+self.sale_order+ self.sent+self.locked+self.cancel
    # @api.one
    # def all_count(self):
    #     count = self.env['sale.order'].search_count(['partner_id','=','True'])
    #     self.all = count

#quotation######
    @api.multi
    def _compute_quotation(self):
        amounts = self.env['sale.order'].read_group([
            ('team_id', 'in', self.ids),
            ('state', '=', 'draft'),
        ], ['count_record', 'team_id'], ['team_id'])
        for rec in amounts:
            self.browse(rec['team_id'][0]).quotation_fil = rec['count_record']

    #sent######
    @api.multi
    def _compute_sent(self):
        amounts = self.env['sale.order'].read_group([
            ('team_id', 'in', self.ids),
            ('state', '=', 'sent'),
        ], ['count_record', 'team_id'], ['team_id'])
        for rec in amounts:
            self.browse(rec['team_id'][0]).sent_fil = rec['count_record']


            # locked######

    @api.multi
    def _compute_locked(self):
        amounts = self.env['sale.order'].read_group([
            ('team_id', 'in', self.ids),
            ('state', '=', 'done'),
        ], ['count_record', 'team_id'], ['team_id'])
        for rec in amounts:
            self.browse(rec['team_id'][0]).locked_fil = rec['count_record']

    #sale######
    @api.multi
    def _compute_cancel(self):
        amounts = self.env['sale.order'].read_group([
            ('team_id', 'in', self.ids),
            ('state', '=', 'cancel'),
        ], ['count_record', 'team_id'], ['team_id'])
        for rec in amounts:
            self.browse(rec['team_id'][0]).cancel_fil = rec['count_record']


    #cancel######
    @api.multi
    def _compute_sale(self):
        amounts = self.env['sale.order'].read_group([
            ('team_id', 'in', self.ids),
            ('state', '=', 'sale'),
        ], ['count_record', 'team_id'], ['team_id'])
        for rec in amounts:
            self.browse(rec['team_id'][0]).sale_orde_filr  = rec['count_record']

class SaleAdvancePaymentInv_inherit(models.TransientModel):
    _inherit = "sale.advance.payment.inv"

    advance_payment_method = fields.Selection([
            ('delivered', 'Invoiceable lines'),
            ], string='Invoice Through', default='delivered', required=True)
