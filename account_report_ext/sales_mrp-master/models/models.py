# -*- coding: utf-8 -*-

from odoo import models, fields, api
import odoo.addons.decimal_precision as dp
from dateconversion import *

# customer model

# class sale_customer(models.Model):
#     _inherit='res.partner'


    # @api.one
    # @api.model
    # @api.depends('contract_start')
    # def _converttonepa(self):
    #     try:
    #         inputdata = str(self.contract_start)
    #         dt = datenepali()
    #         converted_date = dt.converttonepali(inputdata)
    #         self.nep_date = converted_date
    #     except ValueError:
    #         return 'Enter Date.'
    #
    # nep_date = fields.Char(compute='_converttonepa', store=True, string='मिती')






# sales model


class sale_code(models.Model):
    _inherit='sale.order'

    # @api.one
    # @api.model
    # @api.depends('ord_date')
    # def _converttonepa(self):
    #     try:
    #         inputdata = str(self.ord_date)
    #         dt = datenepali()
    #         converted_date = dt.converttonepali(inputdata)
    #         self.or_date = converted_date
    #     except ValueError:
    #         return 'Enter Date.'
    #
    # or_date = fields.Char(compute='_converttonepa', store=True, string='अडर मिती')


    # for xalidating date

    # exp_date = fields.Date(required=True, string='Expiration Date')

    # @api.one
    # @api.model
    # @api.depends('exp_date')
    # def _converttonep(self):
    #     try:
    #         inputdata = str(self.exp_date)
    #         dt = datenepali()
    #         converted_date = dt.converttonepali(inputdata)
    #         self.expp_date = converted_date
    #     except ValueError:
    #         return 'Enter Date.'
    # expp_date = fields.Char(compute='_converttonep', store=True, string='रुजु मिती')





# product model
class products_ext(models.Model):
    _inherit = 'product.template'
    product=fields.Selection(
        [('cement', 'Cement'), ('clinker', 'Clinker'),('gypsum', 'Gypsum'),('slag', 'Slag'),('flyash', 'Flyash')],
        default='cement', string='Product', required='True')
    mrp = fields.Float(string='Marked Price')
    mrp_total = fields.Float(string='Marked Price Total',compute='_mrp_total',default=1.0)
    vat = fields.Float(string='VAT')
    excise_duty = fields.Float(string='Excise Duty')
    discount = fields.Float(string='Discount')
    # sales_price = fields.Float(compute='_value_pc', store='True', string='Sale Price')
    list_price = fields.Float(
        'Sale Price', default=1.0,
        digits=dp.get_precision('Product Price'),compute='_value_pc',
        help="Base price to compute the customer price. Sometimes called the catalog price.")

    @api.one
    @api.depends('mrp','discount')
    def _mrp_total(self):
        self.mrp_total = float(self.mrp)- float(self.discount)


    @api.one
    @api.depends('mrp_total','vat','excise_duty','discount')
    def _value_pc(self):
        # self.ensure_one()
        # self.vat=2
        if self.vat > 0:
            ab = float(self.mrp_total) / float(self.vat)
            self.list_price = ab - float(self.excise_duty)+float(self.discount)

        # self.data_update()

    # # data mapping1 ###
    # @api.multi
    # def data_update(self):
    #     self.ensure_one()
    #     rec = self.env['sale.order.line'].search([('product_id', '=', self.name)])
    #     if rec:
    #         rec.price_unit = self.sales_price



