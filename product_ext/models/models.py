# -*- coding: utf-8 -*-

from odoo import models, fields, api

class materail_type(models.Model):
    _name = 'material.type'
    _rec_name='material_name'
    material_name=fields.Char(string="Material Type")

    rfq_fil = fields.Integer(compute='_compute_rfq')
    rfq_send_fil = fields.Integer(compute='_compute_rfq_send')
    to_approve_fil = fields.Integer(compute='_compute_to_approve')
    confirmed_fil = fields.Integer(compute='_compute_confirmed')
    locked_fil = fields.Integer(compute='_compute_locked')
    cancelled_fil = fields.Integer(compute='_compute_cancelled')
    color = fields.Integer('Color Index')


    # draft######
    @api.multi
    def _compute_rfq(self):
        amounts = self.env['purchase.order'].read_group([
            ('material_type', 'in', self.ids),
            ('state', '=', 'draft'),
        ], ['count_record', 'material_type'], ['material_type'])
        for rec in amounts:
            self.browse(rec['material_type'][0]).rfq_fil = rec['count_record']

            # sent######

    @api.multi
    def _compute_rfq_send(self):
        amounts = self.env['purchase.order'].read_group([
            ('material_type', 'in', self.ids),
            ('state', '=', 'sent'),
        ], ['count_record', 'material_type'], ['material_type'])
        for rec in amounts:
            self.browse(rec['material_type'][0]).rfq_send_fil = rec['count_record']

            # to_approve######

    @api.multi
    def _compute_to_approve(self):
        amounts = self.env['purchase.order'].read_group([
            ('material_type', 'in', self.ids),
            ('state', '=', 'to_approve'),
        ], ['count_record', 'material_type'], ['material_type'])
        for rec in amounts:
            self.browse(rec['material_type'][0]).to_approve_fil = rec['count_record']

            # purchase######

    @api.multi
    def _compute_confirmed(self):
        amounts = self.env['purchase.order'].read_group([
            ('material_type', 'in', self.ids),
            ('state', '=', 'purchase'),
        ], ['count_record', 'material_type'], ['material_type'])
        for rec in amounts:
            self.browse(rec['material_type'][0]).confirmed_fil = rec['count_record']





            # done######

    @api.multi
    def _compute_locked(self):
        amounts = self.env['purchase.order'].read_group([
            ('material_type', 'in', self.ids),
            ('state', '=', 'cancel'),
        ], ['count_record', 'material_type'], ['material_type'])
        for rec in amounts:
            self.browse(rec['material_type'][0]).locked_fil = rec['count_record']

    # cancel######
    @api.multi
    def _compute_cancelled(self):
        amounts = self.env['purchase.order'].read_group([
            ('material_type', 'in', self.ids),
            ('state', '=', 'cancel'),
        ], ['count_record', 'material_type'], ['material_type'])
        for rec in amounts:
            self.browse(rec['material_type'][0]).cancelled_fil = rec['count_record']

class product_template(models.Model):
    _inherit="product.template"
    material_name=fields.Many2one('material.type',string="Material Type")

    def product_product_data(self):
        for rec in self.order_line:
            dept = rec.env['product.product'].search(
                [("id", '=', self.product_tmpl_id)]
            )
            self.material_name =dept.material_name

class product_product_inherit(models.Model):
    _inherit='product.product'
    material_name=fields.Char(string="Material Type")


