# -*- coding: utf-8 -*-

from odoo import models, fields, api

class _proforma_invoice(models.Model):
    _name = 'proforma.invoice'
    _description = 'Performa Invoice'
    pro_id=fields.One2many('proforma.id','p_id')
    p_date=fields.Date(string="Date")
    ref = fields.Char(string="Reference")
    pu_no=fields.Integer(string="PO no.")
    cus_name = fields.Char(string="Customer Name")
    add = fields.Char(string="Address")



class _prforma_id(models.Model):
    _name = 'proforma.id'
    p_id = fields.Many2one('proforma.invoice')
    sn = fields.Integer(string="S.n")
    des = fields.Char(string="Description")
    quan=fields.Integer(string="Quantity")
    u_p = fields.Float(string="Unit price")
    t_p=fields.Float(string="Total price")




