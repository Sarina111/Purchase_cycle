# -*- coding: utf-8 -*-
from odoo import models, fields, api,_
from odoo.exceptions import ValidationError



class _proforma_invoice(models.Model):
    _name = 'proforma.invoice1'
    _description = 'Proforma Invoice'
    _order='po_no desc'

    pro_date = fields.Date(string="P.I Date")
    partner_id = fields.Many2one('res.partner',string="Vendor Name", readonly=True)
    ven_add = fields.Char(string="Address", readonly=True)
    pi_ref = fields.Char(string="Vendor's P.I No")
    # estimate = fields.Float(string="Estimated Cost")
    estimate = fields.Monetary(string="Estimated Cost",options="{'currency_field': 'currency_id'}")

    currency_id = fields.Many2one('res.currency', string='Currency', required=True, default=lambda self: self.env.user.company_id.currency_id)
    # currency_id = fields.Many2one('res.currency', string='Currency')

    pro_id = fields.One2many('pragyapan.patra1','pro_id')
    po_no = fields.Char(string="PO No.", readonly=True)
    order_date=fields.Date(string='Ordered Date', readonly=True)

    # IC amount for performal invoice
    estimate_ic = fields.Float('Estimated Amount(IC)',readonly=True)
    state = fields.Selection([('draft','Draft'),('sent','Paid')],default='draft')
    prayapan_count = fields.Integer('Pragyapan Count', compute='count_pragyapan_count')
    
    def count_pragyapan_count(self):
        self.pragyapan_count = search.count(self.pra_id)

# sequence id
    name = fields.Char(string='Proforma Invoice ID', copy=False, readonly=True, default=lambda x: _('New'))
    @api.model
    def create(self, values):
        if values.get('name', _('New')) == _('New'):
            values['name'] = self.env['ir.sequence'].next_by_code('proforma.invoice1') or _('New')
        return super(_proforma_invoice, self).create(values)

    # onchange api used on nrp amount, to convert it to ic amount
    @api.onchange('estimate')
    def ic_convert(self):
        self.estimate_ic = self.estimate * 1.60


# creates payment record
    def advance_payment(self):
        self._create_payment()

    @api.multi
    def pro_sent(self):
        self.ensure_one()
        self.write({'state': 'sent'})

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
                'payment_method_id': '4',
                'journal_id':'6',
                'payment_type': 'outbound',
                'partner_type':'supplier',
                'Pol_no':rec.pi_ref


                # 'order_line_id': recoo
            })
        # slip.write({'payment_type': 'out_bound',
        #             'partner_type':'supplier',
        #             'payment_method_id':'2'})
        self.pro_sent()
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
        self.bhada_count = len(self.pra_id)

    @api.model
    def create(self, values):
        if values.get('name', _('New')) == _('New'):
            values['name'] = self.env['ir.sequence'].next_by_code('pragyapan.patra1') or _('New')
        return super(_pragypan_patra, self).create(values)




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
     
        recoo = []
        inv_obj = self.env['proforma.invoice1']

      
        for rec in self:
            slip = inv_obj.create({
                'partner_id': rec.partner_id.id,
                'order_date': rec.date_order,
                'po_no': rec.name,
            })
        return slip

    rfq_vendor_count=fields.Integer('Purchase Count', compute='order_count')


class mrn_inherit(models.Model):
    _inherit='purchase.request'

class account_payment_inherit(models.Model):
    _inherit='account.payment'
    PoI_no=fields.Char(string="Proforma no.")

class hr_employee_inherit(models.Model):
    _inherit='hr.employee'


# bhadachlan

class _bhada_chalan(models.Model):
    _name = 'bhada.chalan1'
    _description = 'Bhada Chalan'

    name = fields.Char(
        'Bhadachalan ID', copy=False, readonly=True, default=lambda x: _('New'))

    prag_id = fields.Many2one('pragyapan.patra1')
    invoice_no=fields.Char(string='INV no')
    invoice_date=fields.Date(string='Invoice Date')
    bc_amount1 = fields.Float("Vehicle Amount", store=True)
    bc_total_amount1 = fields.Float("Final Amount", store=True)
    veh_no1 = fields.Many2one('vehicle.vehicle',string="Vehicle No")
    company = fields.Char( string="Transport Company ")
    mobile = fields.Char(string='Phone')
    driver_name = fields.Char("Driver")
    veh_type1 = fields.Char(string="Vehicle Type")
    bhada_date1 = fields.Date(string="Date")
    driver_lic1 = fields.Char("License No.")
    invoice_line_bhada = fields.One2many('bhadachalan.product', 'bha_id', 'Bhadachalan ID')
    status=fields.Selection([('sales', 'Sales Bhada-Chalan'), ('purchase', 'Purchase Bhada-Chalan')])
    pragyapan_seq_id=fields.Char("Pragyapan ID",related="prag_id.name")


    def bhada_check(self):
        self.ensure_one()
        rec = self.env['checklist.dispatch'].search([('si_no', '=', self.invoice_no)])
        if rec:
            rec.write({'bhada_no': self.name})
    #

    # purchase
    # name1 = fields.Char(
    #     'Purchase_bhadachalan ID', copy=False, readonly=True, default=lambda x: _('New'))
    bill_no = fields.Char( string="Bilty No")
    rate = fields.Float( string="Rate")
    party_wt = fields.Float( string="Party Weight")
    paid_wt = fields.Float( string="Paid Weight")
    wt_exp = fields.Float( string="Weight Expense")
    bc_amount = fields.Float("Vehicle Amount", compute="_compute_amount", store=True)

    @api.depends('rate', 'paid_wt')
    def _compute_amount(self):
        self.bc_amount = float(self.rate) * float(self.paid_wt)

    bc_total_amount = fields.Float("Final Amount", compute="_compute_final_amount", store=True)

    @api.depends('bc_amount', 'wt_exp')
    def _compute_final_amount(self):
        self.bc_total_amount = float(self.bc_amount) - float(self.wt_exp)

    veh_no = fields.Char(string="Vehicle No")
    veh_type = fields.Selection([('truck', 'Truck'), ('tipper', 'Tipper'), ('twelve_wheel', 'Tweleve Wheeler'),
                                 ('sixtn_wheel', 'Sixteen Wheeler'), ('eightn_wheel', 'Eighteen Wheeler')],
                                string="Vehicle Type",)
    trans_name = fields.Char(string="Transportation Company")
    bhada_date = fields.Date(string="Date")
    bhada_driver = fields.Char(string="Driver's Name")
    driver_lic = fields.Char("Driver ID No")

    # @api.model
    # def create(self, values):
    #     if values.get('name', _('New')) == _('New'):
    #         values['name'] = self.env['ir.sequence'].next_by_code('bhada.chalan1') or _('New')
    #     return super(_bhada_chalan, self).create(values)

    # @api.model
    # @api.multi
    # def create(self, values):
    #     # if values.get('name', _('New')) == _('New'):
    #     for rec in self:
    #         # Use the right sequence to set the name
    #         if rec.status== 'purchase':
    #             sequence_code = 'purchase.bhadachalan'
    #         else:
    #             if rec.status=='sales':
    #                 sequence_code = 'sales.bhadachalan'

    #         rec.name = self.env['ir.sequence'].with_context(ir_sequence_date=rec.bhada_date1).next_by_code(sequence_code)
    #         return super(_bhada_chalan, self).create(rec.name)


    @api.model
    def create(self, values):
        object = super(_bhada_chalan, self).create(values)
        object.post()
        return object

    @api.multi
    def post(self):
        for rec in self:
            # Use the right sequence to set the name
            if rec.status== 'purchase':
                sequence_code = 'purchase.bhadachalan'
            else:
                if rec.status=='sales':
                    sequence_code = 'sales.bhadachalan'

            rec.name = self.env['ir.sequence'].with_context(ir_sequence_date=rec.bhada_date1).next_by_code(sequence_code)
            return rec.name

    # @api.model
    # def create(self, values):
    #     for rec in self:
    #         if rec.status == 'sales':
    #             sequence_code = 'sales.bhadachalan'
    #         elif rec.status=='purcahse':
    #             sequence_code = 'purchase.bhadachalan'
    #         values['name'] = self.env['ir.sequence'].next_by_code(sequence_code)
    #         return super(_bhada_chalan, self).create(values)


            # overwrite save function

    # @api.model
    # def create(self, values):
    #     object = super(Checklist, self).create(values)
    #     object._generate_check()
    #     return object

class product_tree(models.Model):
    _name = 'bhadachalan.product'
    _description = 'bhadachalan tree'
    bha_id = fields.Many2one('bhada.chalan1', string='Bhadachalan ID')
    sno = fields.Char("S.No")
    product_id = fields.Char("Product", store=True)
    # invoice_line = fields.One2many('account.invoice.line','invoice_line_ids', string="Invoice Lines")
    quantity = fields.Char("Quantity", store=True)
    remarks = fields.Char("Remarks", store=True)