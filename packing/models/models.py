# -*- coding: utf-8 -*-

from odoo import models, fields, api,_
from odoo.exceptions import ValidationError

class _packing(models.Model):
    _name = 'pack.packing'
    _description = 'packing information'
    _order='create_date desc'
    invoice_line_ids = fields.One2many('packing.product', 'pk_id', 'Packing ID')

    name = fields.Char(
        'Packing ID', copy=False, readonly=True, default=lambda x: _('New'))
    partner_id = fields.Char("Customer",store=True)
    order_date = fields.Date("Order Date")
    expiration_date = fields.Date("Expiration Date")
    truck_no=fields.Char("Vehicle No.")
    so_no=fields.Char(string="SO no.",store=True)
    company = fields.Char(string="Transport Company",translate=True)

    driver_name = fields.Char("Driver")
    state = fields.Selection([('draft', 'Draft'),('pack', 'Packing'),  ('done', 'Done'),  ('rejected', 'Rejected') ], default='draft',index=True,track_visibility='onchange',copy=False)
    name_l= fields.Char(string='LDS no.')
    date_in=fields.Datetime(string='Time In')
    date_out = fields.Datetime(string='Time Out')


    @api.multi
    def pack_draft(self):
        self.ensure_one()
        self.write({'state': 'draft'})

    # @api.multi
    # def disp_dhar(self):
    #     self.ensure_one()
    #     # self.disp_load()
    #     self._create_ka()

    # def disp_load(self):
    #     self.ensure_one()
    #     self.write({'state': 'dhar'})

    @api.multi
    def pack_load(self):
        if self.date_in:
            self.ensure_one()
            self.write({'state': 'pack'})
        else:
            raise ValidationError("Please fill Vehicle In field before prceding.")

    @api.multi
    def pack_done(self):
        if self.driver_name and self.truck_no:
            self.ensure_one()
            self.write({'state': 'done'})
            rec = self.env['dharmakata.dharmakata'].search([('so_no', '=', self.so_no)])
            if rec:
                rec.write({'state': 'aload'})
        else:
            raise ValidationError("Please fill Vehicle Out field before prceding.")
        # self._create_dhar_up()

    # def dispatch_done(self):
    #     self.ensure_one()
    #     rec = self.env['sale.order'].search([('name', '=', self.so_no)])
    #     if rec:
    #         rec.typo= 'load_dhar'

    @api.multi
    def pack_reject(self):
        self.ensure_one()
        self.write({'state': 'rejected'})

     # auto generation of serial number ###
    @api.model
    def create(self, values):
        if values.get('name', _('New')) == _('New'):
            values['name'] = self.env['ir.sequence'].next_by_code('pack.packing') or _('New')
        return super(_packing, self).create(values)

    # @api.multi
    # def create_dhar_up2(self):
    #     self.create_dhar_up1()

    # @api.multi
    # def create_dhar_up1(self):
    #     # if self.state=='load':
    #     #     inv_obj = self.env['loading.slip']
    #     #     rec=inv_obj.search(self.so_no=='so_no')
    #     #     if rec:
    #     #         slip=rec.update({
    #     #             'state':'load'
    #     #         })
    #     #     return slip
    #
    #     # if self.state == 'done':
    #     rec = self.env['dharmakata.dharmakata'].search([('so_no', '=', self.so_no)])
    #     if rec:
    #         rec.state = 'aload'


###############################################################
    @api.multi
    def auto_in_pack(self):
        self.ensure_one()
        self._auto_date_time_in()

    @api.multi
    def _auto_date_time_in(self):
        for order in self:
            self.date_in=fields.Datetime.now()

###################################################

    @api.multi
    def auto_out(self):
        self.ensure_one()
        self._auto_date_time_out()

    @api.multi
    def _auto_date_time_out(self):
        for order in self:
            self.date_out = fields.Datetime.now()

                ###################################################


    # many to one relaiton with loading.slip ###

class product_tree(models.Model):
    _name ='packing.product'
    _description = 'packing tree'
    pk_id = fields.Many2one('pack.packing',string='Packing ID')
    sno = fields.Char("S.No")
    product_id = fields.Char("Product Name",store=True,readonly=True)
    silo= fields.Selection([('choose', 'Choose Silo'),('a', 'Silo 1'), ('b', 'Silo 2'), ('c', 'Silo 3'),('d', 'Silo 4') ], default='choose',string='Silo')

    # invoice_line = fields.One2many('account.invoice.line','invoice_line_ids', string="Invoice Lines")
    quantity=fields.Char("Quantity",store=True,readonly=True)
    # total_qty = fields.Float("Total Quantity", compute="_compute_total", store=True, readonly=True)
    #
    # @api.depends('quantity')
    # def _compute_total(self):
    #     for line in self:
    #         line.total_qty += line.quantity
    #

