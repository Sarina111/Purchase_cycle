# -*- coding: utf-8 -*-
from odoo import models, fields, api,_




class _proforma_invoice(models.Model):
    _name = 'proforma.invoice1'
    _description = 'Proforma Invoice'
    _order='po_no desc'

    pro_date = fields.Date(string="P.I Date")
    partner_id = fields.Many2one('res.partner',string="Vendor Name")
    ven_add = fields.Char(string="Address")
    pi_ref = fields.Char(string="Vendor's P.I No")
    # estimate = fields.Float(string="Estimated Cost")
    estimate = fields.Monetary(string="Estimated Cost",options="{'currency_field': 'currency_id'}")

    currency_id = fields.Many2one('res.currency', string='Currency', required=True, default=lambda self: self.env.user.company_id.currency_id)
    # currency_id = fields.Many2one('res.currency', string='Currency')

    pro_id = fields.One2many('pragyapan.patra1','pro_id')
    po_no = fields.Char(string="PO No.")
    order_date=fields.Date(string='Ordered Date')

    # IC amount for performal invoice
    # IC amount for performal invoiceas
    estimate_ic = fields.Float('Estimated Amount(IC)')
    state = fields.Selection([('draft','Draft'),('sent','Pay')])

    # onchange api used on nrp amount, to convert it to ic amount
    @api.onchange('estimate')
    def ic_convert(self):
        self.estimate_ic = self.estimate * 1.60


# creates payment record
    def advance_payment(self):
        self._create_payment()

    @api.multi
    def _create_payment(self):
        #
        # pdb.set_trace()
        # pprint(self)
        recoo = []
        inv_obj = self.env['account.payment']

        # for r in self:
        #     for re in r.order_line:
        #         # i = i + 1
        #         recoo.append((0, 0, {'product_id': re.product_id.name,
        #                              'quantity': re.product_qty,
        #                              'price_unit':re.price_unit
        #                              }))

        for rec in self:
            slip = inv_obj.create({
                'partner_id':rec.partner_id.id,
                'amount': rec.estimate,
                'payment_method_id': '2',
                'journal_id':'7',
                'payment_type': 'outbound',
                'partner_type':'supplier',
                'communication':rec.pi_ref


                # 'order_line_id': recoo
            })
        # slip.write({'payment_type': 'out_bound',
        #             'partner_type':'supplier',
        #             'payment_method_id':'2'})
        return slip


class _pragypan_patra(models.Model):
    _name = 'pragyapan.patra1'
    _description = 'Pragyapan Patra'
    name = fields.Char(
        'Pragyapan Patra ID', copy=False, readonly=True, default=lambda x: _('New'))

    pro_id = fields.Many2one('proforma.invoice1')
    pragya_date = fields.Date(string="Date")
    pragya_type = fields.Selection([('none',''),('dharauti', 'Dharauti'), ('sadasyata', 'Sadasyata'), ('part', 'Part Pragyapan')],string="Pragyapan Type", required=True)
    pragya_no = fields.Char(reuired=True,string="Pragyapan No")
    declaration_fee = fields.Float(required=True,string="Declaration Fee")
    vat_fee = fields.Float(string="VAT Amount")
    duty_fee = fields.Float(string="Total Duty Fee")
    pra_id = fields.One2many('bhada.chalan1','prag_id')
    bhada_count = fields.Integer('Bhada Count', compute='count_bhada_count')

    def count_bhada_count(self):
        # for rec in self.pra_id:

        # x = x + 1
        self.bhada_count = len(self.pra_id)

        # for bha in self:
        #     bha.bhada_count = bha.search_count(
        #         [('id', '=', bha.pra_id)]
        #     )

    @api.model
    def create(self, values):
        if values.get('name', _('New')) == _('New'):
            values['name'] = self.env['ir.sequence'].next_by_code('pragyapan.patra1') or _('New')
        return super(_pragypan_patra, self).create(values)


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

class purchase_inherit(models.Model):
    _inherit='purchase.order'

    # material_type=fields.Many2one('material.type',string="Material Type",compute="_check_material_type",store=True)
    material_type=fields.Many2one('material.type',string="Material Type")
    count_record=fields.Float(string="Count Record",default='1.0')

    # material_type=fields.Char(string="Material Type",compute="_check_material_type",store=True)

    # @api.multi
    # @api.onchange('order_line.product_id')
    # def _check_material_type(self):
    #     for rec in self.order_line:
    #         self.material_type = rec.product_id.material_name
    @api.multi
    def button_confirm(self):
        for order in self:
            if order.state not in ['draft', 'sent']:
                continue
            order._add_supplier_to_product()
            # Deal with double validation process
            if order.company_id.po_double_validation == 'one_step' \
                    or (order.company_id.po_double_validation == 'two_step' \
                                and order.amount_total < self.env.user.company_id.currency_id.compute(
                            order.company_id.po_double_validation_amount, order.currency_id)) \
                    or order.user_has_groups('purchase.group_purchase_manager'):
                order.button_approve()
            else:
                order.write({'state': 'to approve'})
        self._create_proforma()
        return True

# creates proforma invoice
    @api.multi
    def _create_proforma(self):
        #
        # pdb.set_trace()
        # pprint(self)
        recoo = []
        inv_obj = self.env['proforma.invoice1']

        # for r in self:
        #     for re in r.order_line:
        #         # i = i + 1
        #         recoo.append((0, 0, {'product_id': re.product_id.name,
        #                              'quantity': re.product_qty,
        #                              'price_unit':re.price_unit
        #                              }))

        for rec in self:
            slip = inv_obj.create({
                'partner_id': rec.partner_id.id,
                'order_date': rec.date_order,
                # 'expiration_date': rec.validity_date,
                'po_no': rec.name,
                # 'order_line_id': recoo
            })
        # slip.write({'state': 'draft'})
        return slip

class mrn_inherit(models.Model):
    _inherit='purchase.request'

class account_payment_inherit(models.Model):
    _inherit='account.payment'
    PoI_no=fields.Char(string="Proforma no.")

class hr_employee_inherit(models.Model):
    _inherit='hr.employee'


# class kanban_inherit(models.Model):
#     color=


