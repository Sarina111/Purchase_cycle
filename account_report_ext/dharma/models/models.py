# -*- coding: utf-8 -*-

from odoo import models, fields, api,_
# import time
from datetime import datetime, timedelta

class dharmakata_dharmakata(models.Model):
    _name = 'dharmakata.dharmakata'
    _description = 'dharmakata information'
    _order='name desc'
    bh_id1 = fields.One2many('dharmakata.product', 'bh_id', 'Dharmakata ID')
    name = fields.Char(string='Dharmakata ID', copy=False, readonly=True, default=lambda x: _('New'))
    partner_id = fields.Char("Customer")
    so_no = fields.Char("SO no.")
    date = fields.Datetime('Date')
    # datee=fields.
    date12 = fields.Datetime('Date')
    # order_lines = fields.One2many('sale.order.line', 'order_id', string="Order Line")
    bag = fields.Integer(string='No. of Bags')
    b_wt = fields.Char(string='Weight Before Load (kg)')

    a_wt = fields.Float(string='Expected Weight(kg)', compute="_value_gratio", store=True)

    act_wt = fields.Char(string='Weight After Load (kg)',default=0.0)
    total_product = fields.Float("Total Product", compute='dhar_qty', store=True)
    vehicle_no = fields.Char("Truck No.")
    # state = fields.Selection([('draft', 'Draft'), ('load', 'Loading'), ('aload', 'After Loading'), ('reject', 'Reject'), ('done', 'Done') ],
    #                          default='draft')
    state = fields.Selection(
        [('draft', 'Dharmakata In'),('load_dhar', 'Loading'),('aload', 'After Loading'), ('reject', 'Reject'), ('done', 'Done')],
        default='draft')

    dhar_quantity = fields.Float(string='Total Quantity',
                                 store=True,
                                 readonly=True,
                                 compute='dhar_qty',
                                 track_visibility='always')

    order_date = fields.Date("Ordered Date")
    expiration_date = fields.Date("Expiration Date")

    company = fields.Char( string="truck Company",translate=True)

    driver_name = fields.Char("Truck Driver")
    name_l= fields.Char(string='LDS no.')

    wt_diff=fields.Integer(string='Weight difference(Kg)',default=0.0)
    product_type=fields.Selection(
        [('cement', 'Cement'), ('clinker', 'Clinker'),('gypsum', 'Gypsum'),('slag', 'Slag'),('flyash', 'Flyash')],
        default='cement', string='Product Type', required='True')







    @api.multi
    def dhar_draft(self):
        self.ensure_one()
        self.write({'state': 'draft'})

    @api.multi
    def dhar_draft_rej(self):
        self.ensure_one()
        self.write({'state': 'draft'})
        # self.reject_pack()



    # @api.multi
    # def dhar_load(self):
    #     self.ensure_one()
    #     self.write({'state': 'load'})
        # self._create_pack()

        # self.dhar_dispatch()

    # @api.multi
    # def dhar_dispatch(self):
    #     self.ensure_one
    #     # if self.state=='load':
    #     self._create_load_up()
    #     # self.env['loading.slip'].disp_load()

    #
    @api.multi
    def dhar_load(self):
        self.ensure_one()
        self.write({'state': 'load_dhar'})
        self.create_pack()

    @api.multi
    def dhar_aload(self):
        self.ensure_one()
        self.write({'state': 'aload'})

        # self._auto()

    @api.multi
    def dhar_reject(self):
        self.ensure_one()
        self.write({'state': 'reject'})
        self.reject_pack()


    @api.multi
    def dhar_done(self):
        self.ensure_one()
        self.write({'state': 'done'})
        rec = self.env['loading.slip'].search([('so_no', '=', self.so_no)])
        if rec:
            rec.write({'state': 'd_done'})
            rec.write({'dhama_no': self.name})
            # rec.write({'dhar_quantity': self.dhar_quantity})
        self.dha_checklist()

##############################################

    @api.multi
    def dha_checklist(self):
        self.ensure_one()

        rec = self.env['loading.slip'].search([('so_no', '=', self.so_no)])
        if rec:
            rec.write({'dharma_no': self.name})
        ################################################
    #Expected Weight####

    @api.depends('dhar_quantity','b_wt')
    def _value_gratio(self):
        self.a_wt = (float(self.dhar_quantity) * 50) +float(self.b_wt)

#######################################################
    #Difference in weight
    @api.multi
    @api.depends('act_wt', 'a_wt')
    def calc_diff(self):
        self.write({'wt_diff': 0.0})
        if self.state == 'aload':
            if self.act_wt > 0.0:
                self.wt_diff = float(self.act_wt) - float(self.a_wt)
                for record in self:
                    if record.wt_diff < (-50):
                        record.write({'state': 'reject'})
                        rec = record.env['pack.packing'].search([('so_no', '=', record.so_no)])
                        if rec:
                            rec.write({'state': 'rejected'})
                        #
                        # # record.state = 'reject'
                        # record.reject_pack()
        # self.trans_pack()
###########################################################

    # @api.multi
    # @api.depends('wt_diff')
    # def trans_pack(self):
    #     # for record in self:
    #     if self.wt_diff > 5:
    #         # record.dhar_reject()
    #         self.state = 'reject'
    #         # for reco in record:
    #         self.reject_pack()






    @api.multi
    def reject_pack(self):
        self.ensure_one()
        rec = self.env['pack.packing'].search([('so_no', '=', self.so_no)])
        if rec:
            rec.state = 'rejected'
#####################################################################
    #
    # @api.depends('order_line.product_uom_qty')
    # def _compute_bag(self):
    #     for line in self:
    #         line.bag += line.order_line.product_uom_qty
    #

    @api.model
    def create(self, valueeees):
        if valueeees.get('name', _('New')) == _('New'):
            valueeees['name'] = self.env['ir.sequence'].next_by_code('dharmakata.dharmakata') or _('New')
        return super(dharmakata_dharmakata, self).create(valueeees)

    net_wt = fields.Float(string='Quantity Weight', compute="_net_weight", store=True)

    @api.depends('act_wt', 'b_wt')
    def _net_weight(self):
        self.net_wt = float(self.act_wt) -float(self.b_wt)



    @api.depends('bh_id1.quantity')
    def dhar_qty(self):
        dhar_quantity = 0.0

        for order in self:

            for line in order.bh_id1:
                dhar_quantity += line.quantity

        self.update({
            'dhar_quantity':dhar_quantity
        })

    # @api.multi
    # def _create_ka(self):
    #     inv_obj = self.env['loading.slip']
    #
    #
    #     for rec in self:
    #         slip = inv_obj.create({
    #             'opt': rec.opt,
    #
    #         })
    #     slip.write({'state': 'sent'})
    #     return slip

##################
    # @api.onchange(so_no)
    @api.multi
    def _create_load_up(self):
        # if self.state=='load':
        #     inv_obj = self.env['loading.slip']
        #     rec=inv_obj.search(self.so_no=='so_no')
        #     if rec:
        #         slip=rec.update({
        #             'state':'load'
        #         })
        #     return slip

        if self.state == 'aload':
            rec = self.env['loading.slip'].search([('so_no', '=', self.so_no)])
            if rec:
                rec.state = 'load'

        # return rec

#######################################

    @api.multi
    def create_pack(self):
        recoo = []
        inv_obj = self.env['pack.packing']

        for r in self:
            for re in r.bh_id1:
                recoo.append((0, 0, {'product_id': re.product_id,
                                     'quantity': re.quantity,
                                     }))

        for rec in self:
            slip = inv_obj.create({
                'partner_id': rec.partner_id,
                'order_date': rec.order_date,
                'expiration_date': rec.expiration_date,
                'so_no': rec.so_no,
                'truck_no': rec.vehicle_no,
                'company': rec.company,
                'driver_name': rec.driver_name,
                'name_l':rec.name_l,
                # 'state':draft
                'invoice_line_ids': recoo
            })
        slip.write({'state': 'draft'})
        return slip
    # ####################################################################
    @api.multi
    def auto_in(self):
        self.ensure_one()
        self._auto_date_time_in()

    @api.multi
    def _auto_date_time_in(self):
        for order in self:
            self.date = fields.Datetime.now()

    @api.multi
    def auto_out(self):
        self.ensure_one()
        self._auto_date_time()

    @api.multi
    def _auto_date_time(self):
        for order in self:
            self.date12=fields.Datetime.now()

    # @api.multi
    # def _confirmSale(self):
    #     for order in self:
    #         order.salesorder_date = fields.Date.today()  # there's a today() helper on the Date field


#####################################################################



class product_tree(models.Model):
    _name ='dharmakata.product'
    _description = 'dharmakata tree'
    bh_id = fields.Many2one('dharmakata.dharmakata',string='Dharmakata ID')
    # sno = fields.Char("S.No")
    product_id = fields.Char("Product Name")
    # invoice_line = fields.One2many('account.invoice.line','invoice_line_ids', string="Invoice Lines")
    quantity=fields.Float("Quantity")

    total_quantity = fields.Float("Total Quantity", compute="compute_amount", store=True, readonly=True)

    @api.depends('quantity')
    def compute_amount(self):
        for line in self:
            line.total_quantity += line.quantity



