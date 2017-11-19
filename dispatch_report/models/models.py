# -*- coding: utf-8 -*-

from odoo import models, fields, api
from odoo.exceptions import ValidationError

class DispatchReport(models.Model):
    _name = 'dispatch.report'
    si_no = fields.Char('Sales Invoice no')
    bharpai_no = fields.Char('Bharpai no')
    party_name = fields.Char('Party Name')
    party_vat = fields.Char('Party\'s VAT')
    checked_by = fields.Char('Checked by')
    delivery_address = fields.Char('Delivery address')
    # order_line
    prd_brand = fields.Char('Brand Name')
    brand_quantity = fields.Char('Quantity')
    brand_rate = fields.Char('Rate')
    brand_discount = fields.Char('Discount')
    brand_excise = fields.Char('Excise')
    brand_total = fields.Char('Total')
    dispatch_vat = fields.Char('Dispatch VAT')
    truck_no = fields.Char('Truck no')
    vehicle_amount = fields.Char('Vehicle Amount')
    prd_line_id = fields.One2many('daily.dispatchprd', 'dp_id', 'Product Line')
    # agni_qty = fields.Integer('Agni Quantity')
    agni_qty = fields.Char(compute='set_on_fields', string='Agni Quantity')
    alpha_qty = fields.Char(compute='set_on_fields',string='Alpha Quantity')
    orient_qty = fields.Char(compute='set_on_fields',string='Orient Quantity')
    tridev_qty = fields.Char(compute='set_on_fields',string='Tridev Quantity')
    # select_try = fields.Selection[('a','1a'),('b','2b'),('c','3c'),('d','4d'),('e','5e')]
    

    # @api.onchange('prd_line_id')
    def set_on_fields(self):
        for se in self:
            for s in se.prd_line_id:
                if s.product_id == 'Agni':
                    self.agni_qty = s.quantity
                elif s.product_id == 'Alpha':
                    self.alpha_qty = s.quantity
                    # raise ValidationError("Done")
                elif s.product_id == 'Orient':
                    self.orient_qty = s.quantity
                elif s.product_id == 'Tridev':
                    self.tridev_qty = s.quantity

    # def compute_bhada_count(self):
    #     for bha in self:
    #         bha.bhada_count = bha.search_count(
    #             [('user_id', '=', bha.user_id.id)]
    #         )

    # bhada_count = fields.Integer('Bhadachalan Count')
    bhada_count = fields.Integer('Bhadachalan Count', default=5
                                 # compute="compute_bhada_count"
    )

    def smart_error(self):
        raise ValidationError('Smart Button')






class DispatchProduct(models.Model):
    _name = 'daily.dispatchprd'
    dp_id = fields.Many2one('dispatch.report', 'Dispatch Product')
    product_id = fields.Char('Product ID')
    quantity = fields.Char('Quantity')

class SmartInherit(models.Model):
    _inherit = 'res.partner'
    # use lambda default here
    bhada_count = fields.Integer('Bhada Count',
                                 compute='compute_user_bhada_count')

    def compute_user_bhada_count(self):
        for bhada in self:
            bhada.bhada_count = bhada.search_count(
                [('user_id', '=', bhada.user_id.id)]
            )
    def compute_bhada_count(self):
        sale_data = self.env['bhada.chalan1'].read_group(domain=[('user_id', self.ids)],
                                                      fields=['user_id'], groupby=['user_id'])

        # read to keep the child/parent relation while aggregating the read_group result in the loop
        # user_child_ids = self.read(['child_ids'])
        mapped_data = dict([(m['user_id'][0], m['user_id_count']) for m in sale_data])
        for partner in self:
            # let's obtain the partner id and all its child ids from the read up there
            user_ids = filter(lambda r: r['id'] == user.id, user_child_ids)[0]
            user_ids = [user_ids.get('id')] + user_ids.get('child_ids')
            # then we can sum for all the partner's child
            partner.bhada_count = sum(mapped_data.get(child, 0) for child in user_ids)
        # raise ValidationError(bhada.bhada_count)

# class bharpai_report(models.Model):
#     _name = 'bharpai_report.bharpai_report'

#     name = fields.Char()
#     value = fields.Integer()
#     value2 = fields.Float(compute="_value_pc", store=True)
#     description = fields.Text()
#
#     @api.depends('value')
#     def _value_pc(self):
#         self.value2 = float(self.value) / 100
