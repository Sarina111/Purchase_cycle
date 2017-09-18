# -*- coding: utf-8 -*-

from odoo import models, fields, api

class _pragypan_patra(models.Model):
    _name = 'pragyapan.patra'
    _description = 'Pragyapan Patra'
    pro_id=fields.One2many('pragyapan.id','p_id')


    pra_date=fields.Date(string="Date")
    cus_name = fields.Char(string="Customer Name")
    add = fields.Char(string="Address")

    pu_no=fields.Integer(string="PO no.")
    Pragya_no = fields.Integer(string="Pragyapan no.")
    Sadasyata_no = fields.Integer(string="Sadasyata no.")
    dhaarauti_no = fields.Integer(string="Dharauti no.")
    # pra_type=fields.Selection([('not_started', '--Select Shareholder type--'), ('dharauti', 'Dharauti'), ('sadasyata', 'Sadasyata'), ('part-pra', 'Part Pragyapan'),], default='not_started',string="Pragyapan Type")
    amount = fields.Float(string="Amount of Pragyapan Patra")

class _prforma_id(models.Model):
    _name = 'pragyapan.id'
    p_id = fields.Many2one('pragyapan.patra')
    sn = fields.Integer(string="S.n")
    bill_no = fields.Many2one('bc.bhadachalan',string="Bilty no.")
    veh_no=fields.Char(string="Vehicle Number",related='bill_no.bc_vehicle_number')
    veh_type= fields.Selection(string="Vehicle Type",related='bill_no.bc_type_of_vehicle')
    tra_name=fields.Char(string="Transport Name")
    rate = fields.Float(string="Rate")
    party_wt = fields.Float(string="Party Weight",related='bill_no.bc_send_weight')
    paid_wt = fields.Float(string="Paid Weight",related='bill_no.bc_received_weight')
    wt_exp = fields.Float(string="Weight Expense")