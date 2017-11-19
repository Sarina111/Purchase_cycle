# -*- coding: utf-8 -*-

from odoo import models, fields, api

class _bhada_chalan(models.Model):
    _name = 'bhada.chalan'
    _description = 'Bhada Chalan'

    pra_id = fields.Many2one('pragyapan.patra1')
    bill_no = fields.Char(required=True,string="Bill No")
    rate = fields.Float(required=True,string="Rate")
    party_wt = fields.Float(required=True,string="Party Weight")
    paid_wt = fields.Float(required=True,string="Paid Weight")
    wt_exp = fields.Float(required=True,string="Weight Expense")
    bc_amount = fields.Float("Vehicle Amount", compute="_compute_amount", store=True)

    # ic amount field for bhadachalan
    bc_amount_ic = fields.Float('Vehicle Amount(IC)')

    @api.onchange(bc_amount)
    def ic_converter(self):
        self.bc_amount_ic = self.bc_amount * 1.60

    @api.depends('rate', 'paid_wt')
    def _compute_amount(self):
        self.bc_amount =( float(self.rate) * float(self.paid_wt))-float(self.wt_exp)

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
