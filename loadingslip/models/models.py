# -*- coding: utf-8 -*-

from odoo import models, fields, api,_
import re
from odoo.osv import osv
import requests
from odoo.exceptions import ValidationError

class LoadingSlip(models.Model):
    _name = 'loading.slip'
    _description = 'loading information'
    _order = 'name desc'
    invoice_line_ids = fields.One2many('loading.product', 'bh_id', 'Loading ID')

    name = fields.Char(
        'Loading_slip ID', copy=False, readonly=True, default=lambda x: _('New'))
    partner_id = fields.Char("Customer",store=True)
    order_date = fields.Date("Date")
    expiration_date = fields.Date("Expiration Date")
    truck_no=fields.Many2one('vehicle.vehicle',string="Truck No.")
    vehicle_type=fields.Selection(string='vehicle_Type',related='truck_no.vehicle_type')
    so_no=fields.Char(string="SO no.",store=True)
    # company = fields.Many2one('res.partner',string="ट्रान्सपोट कम्पनी",change_default=True, index=True, track_visibility='always',translate=True)
    # driver_name = fields.Char("ट्रक ड्राइभर")
    # driver_name = fields.Char("ट्रक ड्राइभर")
    driver_name= fields.Many2one('res.partner',string="Driver",)
    driver_add=fields.Char(string='Driver Address',related='driver_name.street')
    key_person = fields.Char(related='company.key_person', string='Key Person')

    license = fields.Char(string='License',related='driver_name.license')
    company = fields.Many2one(string="Transport Company",related='driver_name.parent_id')
    company_phone=fields.Char(string="Company Mobile", related='company.phone')
    mobile_driver=fields.Char(string='Mobile',related='driver_name.mobile')
    ld_date= fields.Datetime('Date', default=fields.Datetime.now)

    dharma_no=fields.Char(string='Dharmakata No')


    state = fields.Selection([('draft', 'Draft'), ('load', 'In Process'),('d_done', 'Dharmakata Done'), ('sent', 'Sent'),('lock', 'Locked'), ], default='draft')





    # @api.multi
    # def validate(self):
    #     while True:
    #         reg = raw_input("Enter vehicle number: ")
    #
    #         a, b, c, d, e, f, g = reg[:2], reg[2:3], reg[3:5], reg[5:6], reg[6:9], reg[9:10], reg[10:]
    #         if all((a.isupper(), b.isspace(), c.isdigit(), d.isspace(), e.isupper(), f.isspace(), g.isdigit(),
    #                 len(g) == 4)):
    #             print("Valid reg")
    #         else:
    #             print("Invalid reg")



    @api.multi
    def disp_draft(self):
        self.ensure_one()
        self.write({'state': 'draft'})

    # @api.multi
    # def disp_dhar(self):
    #     self.ensure_one()
    #     self.write({'state': 'dhar'})
    #     # self.disp_load()
    #     self._create_ka()

    @api.multi
    def disp_draft(self):
        self.ensure_one()
        self.write({'state': 'd_done'})

    @api.multi
    def disp_lock(self):
        self.ensure_one()
        self.write({'state': 'lock'})





    @api.multi
    def disp_load(self):
        if self.driver_name and self.truck_no:
            self.ensure_one()
            self.write({'state': 'load'})
            self._create_ka()
        else:
            raise ValidationError("Please fill all the fields before prceding.")
    # self.update_inv()

    @api.multi
    def disp_sent(self):
        self.ensure_one()
        self.write({'state': 'sent'})
        self.dispatch_done()
        self.update_inv()
        # self.disp_daily_send()

    def disp_daily_send(self):
        ddr_env = self.env['dispatch.report']
        pdt_list = []
        for z in self:
            for pds in z.invoice_line_ids:
                pdt_list.append((0, 0, {'product_id': pds.product_id,
                                        'quantity': pds.quantity
                                        }))
                # recoo.append((0, 0, {'product_id': re.product_id,
                #                      'quantity': re.quantity,
                #                      }))

        for aa in self:
            prd_line = ddr_env.create({
                'si_no': aa.name,
                'party_name': aa.partner_id,
                'prd_line_id': pdt_list
            })
            return prd_line


    def dispatch_done(self):
        self.ensure_one()
        rec = self.env['sale.order'].search([('name', '=', self.so_no)])
        if rec:
            rec.typo= 'done'

     # auto generation of sequence number ###
    @api.model
    def create(self, valueees):
        if valueees.get('name', _('New')) == _('New'):
            valueees['name'] = self.env['ir.sequence'].next_by_code('loading.slip') or _('New')
        return super(LoadingSlip, self).create(valueees)

    @api.multi
    def _create_ka(self):
        # pdb.set_trace()
        # pprint(self)
        # self.write({'state': 'dhar'})
        recoo = []
        inv_obj = self.env['dharmakata.dharmakata']

        for r in self:
            for re in r.invoice_line_ids:
                recoo.append((0, 0, {'product_id': re.product_id,
                                     'quantity': re.quantity,
                                     }))

        for rec in self:
            slip = inv_obj.create({
                'partner_id': rec.partner_id,
                'order_date': rec.order_date,
                'expiration_date': rec.expiration_date,
                'so_no': rec.so_no,
                'vehicle_no': rec.truck_no.id,
                'company':rec.company.name,
                'driver_name':rec.driver_name.name,
                'name_l': rec.name,
                'test1': rec.truck_no.id,
                # 'state':draft
                'bh_id1': recoo

            })
        slip.write({'state': 'draft'})
        return slip

    def update_inv(self):
        self.ensure_one()
        rec = self.env['sale.order'].search([('name', '=', self.so_no)])
        if rec:
            rec.truck_no = self.truck_no.id
            rec.com=self.company.name
            rec.driver_name = self.driver_name.name
            rec.mobile_driver=self.mobile_driver
            rec.license=self.license
            rec.vehicle_type=self.vehicle_type
            rec.dharma_no=self.dharma_no
            rec.driver_add=self.driver_add
            rec.key_person = self.key_person
            rec.company_phone=self.company_phone


    # many to one relaiton with loading.slip ###

class product_tree(models.Model):
    _name ='loading.product'
    _description = 'loading tree'
    bh_id = fields.Many2one('loading.slip',string='Loading ID')
    sno = fields.Char("S.No")
    product_id = fields.Char("Product Name",store=True)
    sailo= fields.Selection([('a', 'Sailo A'), ('b', 'Sailo B'), ('c', 'Sailo C'), ], default='',string='सैलो')

    # invoice_line = fields.One2many('account.invoice.line','invoice_line_ids', string="Invoice Lines")
    quantity=fields.Char("Quantity",store=True)
    # total_qty = fields.Float("Total Quantity", compute="_compute_total", store=True, readonly=True)
    #
    # @api.depends('quantity')
    # def _compute_total(self):
    #     for line in self:
    #         line.total_qty += line.quantity
    #


    # # data mapping ###
    # @api.multi
    # def _create_slip(reco):
    #     inv_obj = reco.env['loading.slip']
    #     reco.ensure_one()
    #     # while (reco.product_id.name != []):
    #     # for rec in reco:
    #     slip_id = inv_obj.create({
    #         'partner_id': reco.partner_id.name,
    #         'order_date': reco.date_order,
    #         'expiration_date': reco.validity_date,
    #         'so_no': reco.name,
    #
    #         'invoice_line_ids': [(0, 0, {
    #                                 'product_id': reco.product_id.name,
    #                                 'quantity': reco.product_uom_qty,
    #                             })],
    #     })
    #     reco.tab()
    #     return slip_id

        # inv_line_list = []
        # for orders in reco.order_line:
        #     inv_line_data = {
        #         'product_id': orders.product_id.name,
        #         'connecting_field': slip_id,
        #         'quantity': orders.product_uom_qty,
        #     }
        #     inv_line_list.append(inv_line_data)
        #
        # inv_line_obj = reco.env['sale.order.line']
        # for data_record in inv_line_list:
        #     return inv_line_obj.create(data_record)


            # return slip_id



        # @api.depends('name')
        # @api.multi
        # def tab(self):
        #     inv_obj = self.env['loading.slip']
        #     while (self.product_id !=[]):
        #         for rec in self.order_line:
        #             slip1 = inv_obj.create({
        #                 'invoice_line_ids': [(4, 'name', {
        #                     'product_id': rec.product_id.name,
        #                     'quantity': rec.product_uom_qty,
        #                 })],
        #             })
        #         return slip1


class sale_inherit(models.Model):
    _inherit='sale.order'

class Checklist(models.Model):
    _name ='checklist.dispatch'
    _order = 'name desc'
    dharma_doc=fields.Boolean(string='Dharmakata Document',required=True)
    bhadachalan_doc = fields.Boolean(string='Bhadachalan Document',required=True)
    invoice_doc = fields.Boolean(string='Invoice Document',required=True)


    partner_id = fields.Char("Customer")
    invoice_date = fields.Date("Invoice Date")
    truck_no = fields.Char("Vehicle No.")
    company = fields.Char(string="Transport Company")
    mobile_driver=fields.Char(string='Mobile')

    driver_name = fields.Char("Driver")
    si_no = fields.Char("SI No.")
    so_no = fields.Char("SO No.")
    invoice_line_checklist = fields.One2many('checklist.product', 'ch_id', 'Loading ID')
    bhada_no=fields.Char(string='Bhadachalan no.')
    dharma_no=fields.Char(string='Dharmkata no.')
    sales_mobile = fields.Char()
    customer_mobile = fields.Char()
    state = fields.Selection([('draft', 'Gatepass pending'), ('sent', 'Gatepass Created')],default='draft')



    # auto generation of serial number ###
    # @api.model
    # def create(self, valueees):
    #     if valueees.get('name', _('New')) == _('New'):
    #         valueees['name'] = self.env['ir.sequence'].next_by_code('gate.pass') or _('New')
    #     return super(_gatepass, self).create(valueees)


    name = fields.Char(
        'Check List ID', copy=False, readonly=True, default=lambda x: _('New'))
    # auto generation of serial number ###
    @api.model
    def create(self, values):
        if values.get('name', _('New')) == _('New'):
            values['name'] = self.env['ir.sequence'].next_by_code('checklist.dispatch') or _('New')
        return super(Checklist, self).create(values)



    @api.multi
    def create_pass(self):
        recoo = []
        inv_obj = self.env['gate.pass']
        # i = -1
        for r in self:
            for re in r.invoice_line_checklist:
                # i = i + 1
                recoo.append((0, 0, {'product_id': re.product_id,
                                     'quantity': re.quantity,
                                     }))
        for rec in self:
            slip = inv_obj.create({
                'partner_id': rec.partner_id,
                'invoice_date': rec.invoice_date,
                # 'expiration_date': rec.validity_date,
                'truck_no': rec.truck_no,
                'company': rec.company,
                'driver_name': rec.driver_name,
                # 'mobile_driver': rec.customer_mobile,
                'customer_mobile': rec.customer_mobile,
                'bhada_no':rec.bhada_no,
                # 'mobile':rec.mobile,
                'sales_mobile': rec.sales_mobile,
                'si_no': rec.si_no,
                'invoice_line_pass': recoo
            })
        self.write({'state': 'sent'})
        return slip






        # many to one relaiton with loading.slip ###


class check_tree(models.Model):
    _name = 'checklist.product'
    ch_id = fields.Many2one('checklist.dispatch', string='Bharpai ID')
    sno = fields.Char("S.No")
    product_id = fields.Char("Product", store=True)
    # invoice_line = fields.One2many('account.invoice.line','invoice_line_ids', string="Invoice Lines")
    quantity = fields.Char("Quantity", store=True)


class vehicle(models.Model):
    _name='vehicle.vehicle'
    _rec_name='vehicle_number'
    vehicle_number = fields.Char(required=True, string='Vehicle No')
    vehicle_type = fields.Selection([('truck', 'Truck'), ('tipper', 'Tipper'),('tractor', 'Tractor'),
                                     ('six_wheel', 'Six Wheel'), ('ten_wheel','Ten Wheel'), ('twelve_wheel', 'Tweleve Wheeler'),
                                     ('fourteen_wheel', 'Fourteen Wheeler'), ('sixtn_wheel', 'Sixteen Wheeler'),
                                     ('eightn_wheel', 'Eighteen Wheeler'), ('twenty_wheel','Twenty Wheel')],
                                    string="Vehicle Type", required=True)
    remarks = fields.Text(string='Remarks')

    name = fields.Char(
        'Vehicle ID', copy=False, readonly=True, default=lambda x: _('New'))

    # auto generation of serial number ###
    @api.model
    def create(self, values):
        if values.get('name', _('New')) == _('New'):
            values['name'] = self.env['ir.sequence'].next_by_code('checklist.product') or _('New')
        return super(vehicle, self).create(values)

    @api.onchange('vehicle_number')
    def change_to_ucase(self):
        if self.vehicle_number:
            self.vehicle_number = str(self.vehicle_number).upper()

    # @api.constrains('vehicle_number')
    # def validate(self):
    #     while True:
    #         a, b, c, d, e, f, g =self.vehicle_number[:2], self.vehicle_number[2:3], self.vehicle_number[3:5], self.vehicle_number[5:6], self.vehicle_number[6:9], self.vehicle_number[9:10], self.vehicle_number[10:]
    #         if all((a.isupper(), b.isspace(), c.isdigit(), d.isspace(), e.isupper(), f.isspace(), g.isdigit(),
    #                 len(g) == 4)):
    #             return True
    #         else:
    #             raise osv.except_osv('Invalid Number', 'Please enter a valid Truck Number')
    #

    # @api.onchange('vehicle_number')
    # def onchange_case(self):
    #     result = {'value': {
    #         'default_code': str(self.vehicle_number).upper()
    #     }
    #     }
    #
    #     return result


######################################################################
# gatepass
class _gatepass(models.Model):
    _name = 'gate.pass'
    _description = 'gatepass information'
    _order = 'name desc'
    partner_id = fields.Char("Customer")
    mobile_driver = fields.Char(string='Driver Mobile')
    invoice_date = fields.Date("Invoice Date")
    # invoice_line = fields.One2many('account.invoice.line','invoice_line_ids', string="Invoice Lines")
    truck_no=fields.Char("Vehicle No.")
    company = fields.Char( string="Transport Company")

    driver_name = fields.Char("Driver")
    si_no=fields.Char("SI No.")
    bhada_no = fields.Char(string='Bhadachalan no.')
    invoice_line_pass = fields.One2many('gatepass.product', 'bh_id', 'Loading ID')
    name = fields.Char(
        'Loading_slip ID', copy=False, readonly=True, default=lambda x: _('New'))

    state = fields.Selection([('draft','SMS Pending'),('sent','SMS Sent')],default='draft')
    states = fields.Selection([('draft', 'SMS Pending'), ('sent', 'SMS Sent')])
    sales_mobile = fields.Char()
    customer_mobile = fields.Char()


    def post_msg(self):
        self.post_customer_msg()
        self.post_sales_msg()

    # sms to customer
    @api.depends('mobile')
    def post_customer_msg(self):
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
                'to': self.customer_mobile,
                # 'text': 'This is test message'
                'text': 'Dear Customer, Your order on its way.'
            }
        )
        # self.sms_trigger_gatepass()
        # self.gatepass_state()
        return r

    # sms to sales person
    @api.depends('sales_mobile')
    def post_sales_msg(self):
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
                'to': self.sales_mobile,
                # 'text': 'This is test message'
                'text': 'Dear Salesperson, the sales order under your supervision has been sent for gatepass.'
            }
        )
        # self.sms_trigger_gatepass()
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


#############################################################
#  bhadachalan_sales

# class _bhada_chalan(models.Model):
#     _name = 'bhada.chalan1'
#     _description = 'Bhada Chalan'
#     _order='name desc'

#     # pra_id = fields.Many2one('pragyapan.patra1')
#     # bill_no = fields.Char(required=True,string="Bill No")
#     name = fields.Char(
#         'Loading_slip ID', copy=False, readonly=True, default=lambda x: _('New'))
#     invoice_no=fields.Char(string='INV no')
#     invoice_date=fields.Date(string='Invoice Date')

#     # rate1 = fields.Float(string="Rate")
#     # party_wt = fields.Float(required=True,string="Party Weight")
#     # paid_wt = fields.Float(required=True,string="Paid Weight")
#     # wt_exp11 = fields.Float(string="Weight Expense")
#     # bc_amount = fields.Float("Vehicle Amount", compute="_compuSSte_amount", store=True)


#     # @api.depends('rate', 'paid_wt')
#     # def _compute_amount(self):
#     #     self.bc_amount =(float(self.rate) * float(self.paid_wt))-float(self.wt_exp)

#     # bc_total_amount = fields.Float("Final Amount", compute="_compute_final_amount", store=True)
#     bc_amount1 = fields.Float("Vehicle Amount", store=True)
#     advance_amount = fields.Float("Advance Amount", store=True)
#     bc_total_amount1 = fields.Float("Final Amount",compute='_compute_final_amount', store=True)
#     dharma_no = fields.Char(string='Dharma No')
#     rate=fields.Float(string='Rate',compute='calc_vehicle_amount')
#     status=fields.Selection([('sales', 'Sales Bhada-Chalan'), ('purchase', 'Purchase Bhada-Chalan')])


#     def calc_vehicle_amount(self):
#         self.bc_amount1=(self.rate/200) *self.total_quantity


#     @api.depends('bc_amount1', 'advance_amount')
#     def _compute_final_amount(self):
#         self.bc_total_amount1 = float(self.bc_amount1) - float(self.advance_amount)

#     veh_no1 = fields.Char(string="Vehicle No")
#     company = fields.Char( string="Transport Company")
#     company_phone = fields.Char(string="Company Mobile")
#     mobile_driver = fields.Char(string='Driver mobile')

#     driver_name = fields.Char("Driver")
#     veh_type1 = fields.Char(string="Vehicle Type")

#     bhada_date1 = fields.Date(string="Date")

#     driver_lic1 = fields.Char("License No.")
#     driver_add = fields.Char(string='Driver Address')
#     key_person = fields.Char(string='Key Person')

#     invoice_line_bhada = fields.One2many('bhadachalan.product', 'bha_id', 'Bhadachalan ID')
#     total_quantity=fields.Float(string='Total Quantity',store=True,
#                                  readonly=True,
#                                  compute='compute_total_quantity')

#     def bhada_check(self):
#         self.ensure_one()
#         rec = self.env['checklist.dispatch'].search([('si_no', '=', self.invoice_no)])
#         if rec:
#             rec.write({'bhada_no': self.name})

#     @api.multi
#     def auto_in(self):
#         self.ensure_one()
#         self._auto_date_time_in()

#     @api.multi
#     def _auto_date_time_in(self):
#         for order in self:
#             self.bhada_date1 = fields.Datetime.now()

#     @api.model
#     def create(self, values):
#         if values.get('name', _('New')) == _('New'):
#             values['name'] = self.env['ir.sequence'].next_by_code('bhada.chalan1') or _('New')
#         return super(_bhada_chalan, self).create(values)

#     @api.depends('invoice_line_bhada.quantity')
#     def compute_total_quantity(self):
#         total_quantity = 0.0

#         for order in self:
#             for line in order.invoice_line_bhada:
#                 total_quantity += line.quantity
#         self.update({
#             'total_quantity': total_quantity
#         })

class product_tree(models.Model):
    _name = 'bhadachalan.product'
    _description = 'bhadachalan tree'
    bha_id = fields.Many2one('bhada.chalan1', string='Bhadachalan ID')
    sno = fields.Char("S.No")
    product_id = fields.Char("Product", store=True)
    quantity = fields.Float("Quantity", store=True)
    remarks = fields.Char("Remarks", store=True)