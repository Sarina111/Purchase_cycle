# -*- coding: utf-8 -*-
from openerp import models, fields, api, _
import re

import math
from odoo.exceptions import ValidationError

class Client(models.Model):
        _name = 'kyc.clients'
        _rec_name = 'Name'
        _description = 'Main class of kyc'
        _inherit = ['mail.thread']
        name = fields.Char('Client ID', copy=False, readonly=True, default=lambda x: _('New'))
        Client_id = fields.One2many('kyc.legal','Client_id',string='Client_id')
        Client_type = fields.Many2one('client.type',string='Client Type')
        Business_type = fields.Selection([('not_started', '--Select Business type--'),
                                         ('manufacturing', 'Manufacturing'), ('trading', 'Trading'),
                                         ('import/export', 'Import/Export'), ('retailing', 'Retailing'),
                                         ('professional', 'Professional'), ('educational', 'Education',),
                                         ('catering/restaurant', 'Catering/Restaurant'),('service industry', 'Service Industry'),
                                         ('others', 'Others'),],
                                        default='manufacturing')
        Name = fields.Many2one('res.partner',required=True,string='Name')
        related_name = fields.Many2one('res.partner',string='Related Business')
        # related_business = fields.


        # Create unique id of every service record
        @api.model
        def create(self, vals):
                if vals.get('name', _('New')) == _('New'):
                        vals['name'] = self.env['ir.sequence'].next_by_code('kyc.clients') or _('New')
                return super(Client, self).create(vals)


        @api.multi
        def _validate_email(self):
                for partner in self:
                        if re.match("^.+\\@(\\[?)[a-zA-Z0-9\\-\\.]+\\.([a-zA-Z]{2,3}|[0-9]{1,3})(\\]?)$",partner.email) == None:
                                return False
                return True

        email = fields.Char(required=True, string='Email address', related='Name.email')
        _constraints = [
                (_validate_email, 'Please enter a valid email address.', ['email']),
        ]

        Contact_no = fields.Char(string='Contact number', required=True, related='Name.phone',size=10)


        Address = fields.Char(string='Address',required=True, related='Name.street')
        Fax = fields.Char(string='Fax number',related='Name.fax')
        Website = fields.Char(string='Website',related='Name.website')
        No_of_shareholder = fields.Integer(string='No. of shareholders')
        Bank_names = fields.Char(string='Name of banks')
        Login_id = fields.One2many('kyc.login','Login_id')
        Law_id = fields.One2many('kyc.legal_law','Law_id')
        Status_id = fields.One2many('kyc.legal_status','Status_id')
        Document_id = fields.One2many('kyc.documents','Document_id')
        Shareholder_id = fields.One2many('kyc.shareholder','Shareholder_id')
        Question_id = fields.One2many('kyc.finance_questions','Question_id')
        Finance_id = fields.One2many('kyc.finance','Finance_id')
        Software_id = fields.One2many('kyc.cis','Software_id')
        Business_id = fields.One2many('kyc.business_contacts','Business_id')
        Plant_id = fields.One2many('kyc.plants','Plant_id')
        Employee_id = fields.One2many('kyc.key_personnel','Employee_id')
        Party_id = fields.One2many('kyc.party','Party_id')
        Event_id = fields.One2many('kyc.major_events','Event_id')


class client_type(models.Model):
    _name = 'client.type'
    _description = 'Client type class of kyc'
    _rec_name = 'Client_type'
    Client_type = fields.Char('Client Type')

# for major event

class Major_events(models.Model):
        _name = 'kyc.major_events'
        _description = 'Major events class of kyc'
        Event_id = fields.Many2one('kyc.clients','Customer')
        Source = fields.Char(string='Source')
        Date_created = fields.Date(required=True,string='Date')
        Details = fields.Text(required=True,string='Details')
        Notes = fields.Text(string='Notes')

# for legal

class Legal(models.Model):
        _name = 'kyc.legal'
        _description = 'Legal class of kyc'
        Client_id = fields.Many2one('kyc.clients','Client id')
        Regd_type = fields.Selection([('not_started', '--Select Registration type--'),
                                     ('company registration', 'Company Registration'),
                                     ('pan', 'PAN'), ('vat', 'VAT'),],
                                    default='not_started')
        Regd_no = fields.Char(required=True,string='Registration number')
        Regd_date = fields.Date(required=True,string='Registration Date')
        Renewal_date = fields.Date(string='Renewal Date')

# for login

class Login(models.Model):
        _name = 'kyc.login'
        _description = 'Login class of kyc'
        Login_id = fields.Many2one('kyc.clients','Login ID')
        Login_type = fields.Selection([('not_started', '--Select Login type--'),
                                      ('ird', 'IRD'), ('ocr', 'OCR'),],
                                     default='not_started')
        Username = fields.Char(required=True,string='Username')
        show_password = fields.Boolean('Show Password')
        Password = fields.Char(required=True,string='Password')
        Remarks = fields.Char(required=True,string='Remarks')
        submission_id = fields.Char(required=True,string='submision')

        

class Legal_law(models.Model):
        _name = 'kyc.legal_law'
        _description = 'Legal law class of kyc'
        Law_id = fields.Many2one('kyc.clients','Law ID')
        Act_type = fields.Selection([('not_started', '--Select Act type--'),
                                    ('insurance', 'Insurance'), ('company act', 'Company Act'),
                                    ('vat act', 'VAT Act'), ('labour act', 'Labour Act'),
                                    ('income tax act', 'Income Tax Act'), ('ca act', 'CA Act'),],
                                   default='not_started')
        Amendement = fields.Char(required=True,string='Amendement of')
        Enrolled_date = fields.Date(required=True,string='Enrolled Date')
        Renewal_date = fields.Date(string='Date of Renewal')


# Legal status

class Legal_status(models.Model):
        _name = 'kyc.legal_status'
        _description = 'Legal status of kyc'
        Status_id = fields.Many2one('kyc.clients','Status ID')
        Capital_type = fields.Selection([('not_started', '--Select Capital type--'),
                                        ('authorized capital', 'Authorized capital'),
                                        ('issued capital', 'Issued capital'),
                                        ('paid up capital', 'Paid up capital'),],
                                       default='not_started')
        No_of_shares = fields.Integer(required=True, string='Number of shares')
        Value_share = fields.Float(required=True, string='Value per share')
        Total_value = fields.Float(compute="_value_pc", store=True, string="Total Value of Shares")
        # Total_value = fields.Float(string="Total Value of Shares")


        @api.multi
        @api.depends('No_of_shares', 'Value_share')
        def _value_pc(self):
            # test.set_trace()
            for value in self:
                value.Total_value = float(value.No_of_shares) * float(value.Value_share)
                return

# For documents

class Documents(models.Model):
        _name = 'kyc.documents'
        _description = 'Documents class of kyc'
        Document_id = fields.Many2one('kyc.clients','Customer')
        Owner = fields.Char(required=True,string='Owner')
        Purpose = fields.Char(required=True,string='Purpose')
        Date_created = fields.Date(required=True,string='Date created')
        Date_modified = fields.Date(string='Date modified')
        up_id = fields.One2many('kyc.upload','upp_id')

        # for multiple uploads

        def import_file(self, cr, uid, ids, context=None):
                fileobj = TemporaryFile('w+')
                fileobj.write(base64.decodestring(data))
                return


class Upload(models.Model):
        _name = 'kyc.upload'
        _description = 'Upload class of kyc'
        upp_id = fields.Many2one('kyc.documents')
        Uploadss = fields.Binary(required=True, string='Upload')

# for shareholder

class Shareholder(models.Model):
    _name = 'kyc.shareholder'
    _description = 'Shareholder class of kyc'
    _rec_name ='Name'
    Shareholder_id = fields.Many2one('kyc.clients','Customer')

    Name = fields.Char(required=True,string='Name')
    Type = fields.Selection([('not_started', '--Select Shareholder type--'),
                            ('general', 'General'), ('bod', 'B.O.D'),
                            ('ceo', 'C.E.O'), ('promoter', 'Promoter'),],
                           default='not_started')
    Email = fields.Char(string='Email')
    Contact_no = fields.Char(string='Contact number')
    Percentage = fields.Float(required=True,string='Percentage')
    Amount_subscribed = fields.Float(required=True,string='Subscribed amount')
    Amount_paid = fields.Float(required=True,string='Paid amount')
    #
    def send_keypers(self):


        if self.Type == 'bod' or self.Type == 'ceo':
            # raise ValidationError('Hello')
            send_obj = self.env['kyc.key_personnel']

            send = send_obj.create({
                'Name': self.Name,
                'Contact_no': self.Contact_no,
                'Email': self.Email
            })
            return send


    def create_name(self):
        inv_obj = self.env['kyc.key_personnel']
        self.ensure_one()
        # test.set_trace()
        for r in self:
            key = inv_obj.create({
                'Name': r.Name,
                    # 'truck_no': self.vehicle_no,
                'Email': r.Email,
                    # 'order_date': self.date_order,
                    # 'expiration_date': self.validity_date,
                'Contact_no': r.Contact_no
                })
            return key

    def create_key(self):
        self.create_name()

# for finance question

class Finance_questions(models.Model):
        _name = 'kyc.finance_questions'
        _description = 'Finance question class of kyc'
        Question_id = fields.Many2one('kyc.clients','Question ID')
        Question = fields.Selection([('not_started', '--Select Question--'),
                                    ('networth', 'Networth of the company is negative for the last 5 years?'),
                                    ('management', 'Does the management have any intention of closing the business?'),
                                    ('obligation', 'Are there any statutory obligations to close the business'),
                                    ('event', 'Have any subsequent events occured'),],
                                   default='not_started')

        Fiscal_year = fields.Selection([('not_started', '--Select Fiscal Year--'),
                                       ('first', '2072/73'), ('second', '2073/74'),
                                       ('third', '2074/75'), ('fourth', '2075/76'),],
                                      default='not_started')
        Remarks = fields.Text(string='Remarks')
        Answer = fields.Selection([('yes','Yes'),('no','No')],'Answer')


# for finance

class Finance(models.Model):
        _name = 'kyc.finance'
        _description = 'Finance class of kyc'
        Finance_id = fields.Many2one('kyc.clients','Finance ID')
        Particulars = fields.Selection(
                [('register_capital', 'Registered Capital'), ('reserve_surplus', 'Reserve and Surplus'),
                 ('long_term_loan', 'Long Term Loan'), ('short_term_loan', 'Short Term Loan'),
                 ('fixed_assets', 'Fixed Assets'), ('current_assets', 'Current assets, loan and advanced'),
                 ('current_liabilities', 'Current liabilities and Provisions'),
                 ('deferred_tax', 'Deferred Tax Assets/(Liabilities)'), ('sales', 'Sales/Service'),
                 ('cost_of_goods_sold', 'Cost of goods sold'), ('gross_profit', 'Gross Profit'),
                 ('other_income', 'Other Income'), ('admin_expenses', 'Administrative expenses'),
                 ('financial_expenses', 'Financial Expenses'), ('depreciation', 'Depreciation'),
                 ('net_profit_after_deprection', 'Net Profit after Depreciation'), ('tax_provision', 'Tax Provision'),
                 ('deferred_tax_income', 'Deferred Tax Income/(Expense)'),
                 ('net_profit_after_tax', 'Net Profit after Tax')], default='register_capital')

        Fiscal_year = fields.Selection([('not_started', '--Select Fiscal Year--'),
                                       ('first', '2072/73'), ('second', '2073/74'),
                                       ('third', '2074/75'), ('fourth', '2075/76'),],
                                      default='not_started')
        Ratio = fields.Char(string='Ratio')

        gross_profit = fields.Float(required=True, string='Gross Profit')
        sales = fields.Float(required=True, string='Sales')
        net_profit = fields.Float(required=True, string='Net Profit')
        profit_before = fields.Float(required=True, string='Profit before interest')
        finance_expension = fields.Float(required=True, string='Finanace expension')
        share_capital = fields.Float(required=True, string='Share Capital')
        reserve = fields.Float(required=True, string='Reserve and Surplus')
        current_assets = fields.Float(required=True, string='Current assests')
        current_liabilities = fields.Float(required=True, string='Current Liabilities')
        long_debt = fields.Float(required=True, string='Long term Debt')
        share_fund = fields.Float(required=True, string='Shareholders fund')

        gross_profit_ratio = fields.Float(compute='_value_gratio', store=True, string='Gross Profit Ratio')
        net_profit_ratio = fields.Float(compute='_value_nratio', store=True, string='Net Profit Ratio')
        interest_ratio = fields.Float(compute='_value_iratio', store=True, string='Interest Coverage Ratio')
        shareholder_fund = fields.Float(compute='_value_fund', store=True, string='Shareholders fund')
        current_ratio = fields.Float(compute='_value_cratio', store=True, string='Current Ratio')
        debt_equity_ratio = fields.Float(compute='_value_dratio', store=True, string='Debt to Equity Ratio')


# Calculation of different ratios


        @api.depends('gross_profit', 'sales')
        def _value_gratio(self):
            for value in self:
                if value.sales > 0:
                        value.gross_profit_ratio = float(value.gross_profit) / float(value.sales)

        @api.depends('net_profit', 'sales')
        def _value_nratio(self):
            for value in self:
                if value.sales > 0:
                        value.net_profit_ratio = float(value.net_profit) / float(value.sales)

        @api.depends('profit_before', 'finance_expension')
        def _value_iratio(self):
            for value in self:
                if value.finance_expension > 0:
                        value.interest_ratio = float(value.profit_before) / float(value.finance_expension)

        @api.depends('share_capital', 'reserve')
        def _value_fund(self):
            for value in self:
                value.shareholder_fund = float(value.share_capital) + float(value.reserve)

        @api.depends('current_assets', 'current_liabilities')
        def _value_cratio(self):
            for value in self:
                value.current_ratio = float(value.current_assets) - float(value.current_liabilities)

        @api.depends('long_debt', 'share_fund')
        def _value_dratio(self):
            for value in self:
                if value.share_fund > 0:
                        value.debt_equity_ratio = float(value.long_debt) / float(value.share_fund)

# For CIS


class CIS(models.Model):
        _name = 'kyc.cis'
        _description = 'CIS class of kyc'
        Software_id = fields.Many2one('kyc.clients','Customer')
        Department_id = fields.Many2one('hr.department','Department ID')
        Software_type = fields.Selection([('not_started', '--Select Software type--'),
                                         ('accounting', 'Accounting'), ('sales', 'Sales'),],
                                        default='not_started')
        Name = fields.Char(required=True,string='Software name')
        Version_no = fields.Char(string='Version')
        Billing = fields.Selection([('manual','Manual'),('automized','Automized')],'Billing')

# for buiness contacts

class Business_contacts(models.Model):
        _name = 'kyc.business_contacts'
        _description = 'Business contacts class of kyc'
        Business_id = fields.Many2one('kyc.clients','Business ID')
        Component_type = fields.Selection([('not_started', '--Select Component type--'),
                                          ('product', 'Products'), ('service', 'Services'),
                                          ('purchase', 'Purchases'),], default='not_started')
        Component_name = fields.Char(required=True,string='Component name')
        Contact_type = fields.Selection([('not_started', '--Select Contact type--'),
                                        ('customer', 'Customer'), ('vendor', 'Vendor'),],
                                       default='not_started')
        Contact_name = fields.Char(required=True,string='Contact name')
        Address = fields.Char(string='Address')
        Telephone_no = fields.Char(string='Contact number')
        PAN_no = fields.Char(required=True,string='PAN number',size=9)
        Market = fields.Char(string='Major markets')

# For plants

class Plants(models.Model):
        _name = 'kyc.plants'
        _description = 'Plants class of kyc'
        Plant_id = fields.Many2one('kyc.clients','Plant ID')
        Plant_type = fields.Selection([('not_started', '--Select Branch type--'),
                                      ('head office', 'Head office'), ('corporate office', 'Corporate office'),
                                      ('branch', 'Branch'), ('factory', 'Factory'), ('godown', 'Godown'),
                                      ('showroom', 'Showroom'),],
                                     default='not_started')
        Address = fields.Char(required=True,string='Address')
        Supervisor = fields.Many2one('res.partner',string='Supervisor')
        No_of_manpower = fields.Integer(required=True,string='Number of employees')


# for key personnel

class Key_personnel(models.Model):
        _name = 'kyc.key_personnel'
        _description = 'Key personnel class of kyc'
        Employee_id = fields.Many2one('kyc.clients','Employee ID')
        # Name= fields.Many2one('kyc.shareholder',required=True,string='Name')
        Name = fields.Char(string = 'Name')
        Email = fields.Char(required=True,string='Email')
        Contact_no = fields.Char(required=True,string='Contact number')
        Designation = fields.Selection([('not_started', '--Select  Designation--'),
                                       ('ceo', 'C.E.O'), ('proprietor', 'Proprietor'),
                                       ('manager', 'Manager'),],
                                      default='not_started')
        Signatory = fields.Boolean(required=True,string='Signatory?')
        Remuneration_type = fields.Selection([('salaried','Salaried'),('unsalaried','Unsalaried')],string='Remuneration type')



# for party

class Party(models.Model):
        _name = 'kyc.party'
        _description = 'Party class of kyc'
        Party_id = fields.Many2one('kyc.clients','Party ID')
        Name = fields.Char(required=True,string='Party name')
        Tran_type = fields.Char(string='Transaction type')
        Rel_type = fields.Char(string='Relation type')

# for kanaban view

class Kanban(models.Model):
        _inherit = 'kyc.clients'
        _description = 'Kanban class of kyc'
        color = fields.Integer('Color Index')
        priority = fields.Selection(
                [('0', 'Low'),
                 ('1', 'Normal'),
                 ('2', 'High')],
                'Priority', default='1')
