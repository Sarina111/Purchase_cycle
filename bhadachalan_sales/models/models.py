# -*- coding: utf-8 -*-

from odoo import models, fields, api,_

class _bhada_chalan(models.Model):
    _name = 'bhada.chalan1'
    _description = 'Bhada Chalan'

    # pra_id = fields.Many2one('pragyapan.patra1')
    # bill_no = fields.Char(required=True,string="Bill No")
    name = fields.Char(
        'Loading_slip ID', copy=False, readonly=True, default=lambda x: _('नँया'))
    invoice_no=fields.Char(string='INV no')
    invoice_date=fields.Date(string='Invoice Date')

    # rate1 = fields.Float(string="Rate")
    # party_wt = fields.Float(required=True,string="Party Weight")
    # paid_wt = fields.Float(required=True,string="Paid Weight")
    # wt_exp11 = fields.Float(string="Weight Expense")
    # bc_amount = fields.Float("Vehicle Amount", compute="_compuSSte_amount", store=True)
    bc_amount1 = fields.Float("Vehicle Amount", store=True)

    # @api.depends('rate', 'paid_wt')
    # def _compute_amount(self):
    #     self.bc_amount =(float(self.rate) * float(self.paid_wt))-float(self.wt_exp)

    # bc_total_amount = fields.Float("Final Amount", compute="_compute_final_amount", store=True)
    bc_total_amount1 = fields.Float("Final Amount", store=True)

    #
    # @api.depends('bc_amount', 'wt_exp')
    # def _compute_final_amount(self):
    #     self.bc_total_amount = float(self.bc_amount) - float(self.wt_exp)

    veh_no1 = fields.Char(string="Vehicle No")
    company = fields.Char( string="Transport Company ")
    mobile = fields.Char(string='Phone')

    driver_name = fields.Char("Driver")
    veh_type1 = fields.Char(string="Vehicle Type")

    bhada_date1 = fields.Date(string="Date")

    driver_lic1 = fields.Char("License No.")
    invoice_line_bhada = fields.One2many('bhadachalan.product', 'bha_id', 'Bhadachalan ID')

    def bhada_check(self):
        self.ensure_one()
        rec = self.env['checklist.dispatch'].search([('si_no', '=', self.invoice_no)])
        if rec:
            rec.write({'bhada_no': self.name})

    @api.model
    def create(self, values):
        if values.get('name', _('New')) == _('New'):
            values['name'] = self.env['ir.sequence'].next_by_code('bhada.chalan1') or _('New')
        return super(_bhada_chalan, self).create(values)

class product_tree(models.Model):
    _name = 'bhadachalan.product'
    _description = 'bhadachalan tree'
    bha_id = fields.Many2one('bhada.chalan1', string='Bhadachalan ID')
    sno = fields.Char("S.No")
    product_id = fields.Char("Product", store=True)
    # invoice_line = fields.One2many('account.invoice.line','invoice_line_ids', string="Invoice Lines")
    quantity = fields.Char("Quantity", store=True)
    remarks = fields.Char("Remarks", store=True)