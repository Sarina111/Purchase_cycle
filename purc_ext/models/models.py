# -*- coding: utf-8 -*-
from odoo import models, fields, api

class _proforma_invoice(models.Model):
    _name = 'proforma.invoice1'
    _description = 'Proforma Invoice'

    pro_date = fields.Date(required=True,string="P.I Date")
    cust_name = fields.Char(required=True,string="Customer Name")
    cust_add = fields.Text(required=True,string="Address")
    pi_ref = fields.Char(required=True,string="Vendor's P.I No")
    po_no = fields.Char(required=True,string="PO No.")
    estimate = fields.Float(required=True,string="Estimated Cost")
    pro_id = fields.One2many('pragyapan.patra1','pro_id')

#monetory

class _pragypan_patra(models.Model):
    _name = 'pragyapan.patra1'
    _description = 'Pragyapan Patra'
    pro_id = fields.Many2one('proforma.invoice1')
    pragya_date = fields.Date(string="Date")
    pragya_type = fields.Selection([('none',''),('dharauti', 'Dharauti'), ('sadasyata', 'Sadasyata'), ('part', 'Part Pragyapan')],string="Pragyapan Type", required=True)
    pragya_no = fields.Char(reuired=True,string="Pragyapan No")
    declaration_fee = fields.Float(required=True,string="Declaration Fee")
    vat_fee = fields.Float(string="VAT Amount")
    duty_fee = fields.Float(string="Total Duty Fee")
    pra_id = fields.One2many('bhada.chalan','pra_id')


class _bhada_chalan(models.Model):
    _name = 'bhada.chalan'
    _description = 'Bhada Chalan'

    pra_id = fields.Many2one('pragyapan.patra1')
    bill_no = fields.Char(required=True,string="Bilty No")
    rate = fields.Float(required=True,string="Rate")
    party_wt = fields.Float(required=True,string="Party Weight")
    paid_wt = fields.Float(required=True,string="Paid Weight")
    wt_exp = fields.Float(required=True,string="Weight Expense")
    bc_amount = fields.Float("Vehicle Amount", compute="_compute_amount", store=True)

    @api.depends('rate', 'paid_wt')
    def _compute_amount(self):
        self.bc_amount = float(self.rate) * float(self.paid_wt)

    bc_total_amount = fields.Float("Final Amount", compute="_compute_final_amount", store=True)

    @api.depends('bc_amount', 'wt_exp')
    def _compute_final_amount(self):
        self.bc_total_amount = float(self.bc_amount) - float(self.wt_exp)

    veh_no = fields.Char(required=True,string="Vehicle No")
    veh_type = fields.Selection([('truck', 'Truck'), ('tipper', 'Tipper'), ('twelve_wheel', 'Tweleve Wheeler'), ('sixtn_wheel', 'Sixteen Wheeler'), ('eightn_wheel', 'Eighteen Wheeler')],string="Vehicle Type", required=True)
    trans_name = fields.Char(required=True,string="Transportation Company")
    bhada_date = fields.Date(required=True,string="Date")
    bhada_driver = fields.Char(string="Driver's Name")
    driver_lic = fields.Char("Driver ID No")