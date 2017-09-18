# -*- coding: utf-8 -*-

from odoo import models, fields, api,_

class _bharpai(models.Model):
    _name = 'bharpai.bharpai'
    _description = 'bharpai information'
    _order='name desc'
    partner_id = fields.Char("Customer")
    invoice_date = fields.Date("Invoice Date")
    add=fields.Char(string="Address")
    # invoice_line = fields.One2many('account.invoice.line','invoice_line_ids', string="Invoice Lines")
    truck_no=fields.Char("Vehicle No.")
    company = fields.Char( string="Transport Company")

    driver_name = fields.Char("Driver")
    si_no=fields.Char("SI No.")

    invoice_line = fields.One2many('bharpai.product', 'bh_id', 'Loading ID')
    name = fields.Char(
        'Loading_slip ID', copy=False, readonly=True, default=lambda x: _('New'))

    # auto generation of serial number ###
    @api.model
    def create(self, valueees):
        if valueees.get('name', _('New')) == _('New'):
            valueees['name'] = self.env['ir.sequence'].next_by_code('bharpai.bharpai') or _('New')
        return super(_bharpai, self).create(valueees)

        # many to one relaiton with loading.slip ###


class product_tree(models.Model):
    _name = 'bharpai.product'
    _description = 'bharpai tree'
    bh_id = fields.Many2one('bharpai.bharpai', string='Bharpai ID')
    sno = fields.Char("S.No")
    product_id = fields.Char("Product", store=True)
    # invoice_line = fields.One2many('account.invoice.line','invoice_line_ids', string="Invoice Lines")
    quantity = fields.Char("Quantity", store=True)
    price_unit = fields.Float("Unit Price", store=True)
    discount = fields.Float("Discount")
    mrp = fields.Float(string='MRP', compute='_compute_total')
    mrp_subtotal = fields.Float(string='MRP Sub-Total', compute='_compute_total')
    remarks = fields.Char("Remarks", store=True)

    # total_qty = fields.Float("Total Quantity", compute="_compute_total", store=True, readonly=True)
    #
    @api.depends('price_unit', 'discount')
    def _compute_total(self):
        for line in self:
            line.mrp_subtotal = ((line.price_unit - line.discount + 9) * 1.13)
            line.mrp = line.mrp_subtotal + line.discount