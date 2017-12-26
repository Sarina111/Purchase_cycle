# -*- coding: utf-8 -*-

from odoo import models, fields, api,_

class uat_modules(models.Model):
    _name = 'uat.modules'
    _rec_name='module_name'
    module_name=fields.Char(string='Module Name')
    version=fields.Float(string='Version')
    
    module_id=fields.One2many('uat.class','module_id')

    name = fields.Char(
        'Quality Module ID', copy=False, readonly=True, default=lambda x: _('New'))
    # auto generation of serial number ###
    @api.model
    def create(self, values):
        if values.get('name', _('New')) == _('New'):
            values['name'] = self.env['ir.sequence'].next_by_code('uat.modules') or _('New')
        return super(uat_modules, self).create(values)

class uat_class(models.Model):
    _name = 'uat.class'
    _rec_name='class_name'
    class_name=fields.Char(string='Class Name')
    version=fields.Float(string='Version')
    
    module_id=fields.Many2one('uat.modules',string='Module')
    class_id=fields.One2many('uat.testcase','test_id')

    name = fields.Char(
        'Quality Class ID', copy=False, readonly=True, default=lambda x: _('New'))
    # auto generation of serial number ###
    @api.model
    def create(self, values):
        if values.get('name', _('New')) == _('New'):
            values['name'] = self.env['ir.sequence'].next_by_code('uat.class') or _('New')
        return super(uat_class, self).create(values)
    
class uat_testcase(models.Model):
    _name = 'uat.testcase'
    s_n=fields.Integer(string='S.N')
    statement=fields.Char(string='Statement')
    expected_result=fields.Char(string='Expected Result')
    actual_result=fields.Char(string='Actual Result')
   
    test_id=fields.Many2one('uat.test')
    class_id=fields.Many2one('uat.class')
    case_id=fields.One2many('uat.outcomes','case_id')
    
    name = fields.Char(
        'Quality Test Case ID', copy=False, readonly=True, default=lambda x: _('New'))
    # auto generation of serial number ###
    @api.model
    def create(self, values):
        if values.get('name', _('New')) == _('New'):
            values['name'] = self.env['ir.sequence'].next_by_code('uat.testcase') or _('New')
        return super(uat_testcase, self).create(values)


class uat_users(models.Model):
    _name = 'uat.users'
    _rec_name='name'
    name=fields.Char(string='Name')
    organization=fields.Text(string='Organization')

    name = fields.Char(
        'Quality Users ID', copy=False, readonly=True, default=lambda x: _('New'))
    # auto generation of serial number ###
    @api.model
    def create(self, values):
        if values.get('name', _('New')) == _('New'):
            values['name'] = self.env['ir.sequence'].next_by_code('uat.users') or _('New')
        return super(uat_users, self).create(values)


class uat_test(models.Model):
    _name = 'uat.test'
    _rec_name='test_project'
    test_date=fields.Date(string='Date')
    test_project=fields.Char(string='Test Project')
    test_version=fields.Float(string='Test Version')
    uat_module_id=fields.Many2one('uat.modules',string='Module')
    uat_class_id=fields.Many2one('uat.class',string='Class', domain="[('module_id','=',uat_module_id)]")

    test_id=fields.One2many('uat.testcase','test_id')
    name = fields.Char(
        'Quality Test ID', copy=False, readonly=True, default=lambda x: _('New'))
    # auto generation of serial number ###
    @api.model
    def create(self, values):
        if values.get('name', _('New')) == _('New'):
            values['name'] = self.env['ir.sequence'].next_by_code('uat.test') or _('New')
        return super(uat_test, self).create(values)

class uat_outcomes(models.Model):
    _name = 'uat.outcomes'
    _rec_name='test_result'
    test_result=fields.Boolean(string='Test Result')
    test_remarks=fields.Text(string='Test Remarks')
    
    case_id=fields.Many2one('uat.testcase')


    name = fields.Char(
        'Quality Outcomes ID', copy=False, readonly=True, default=lambda x: _('New'))
    # auto generation of serial number ###
    @api.model
    def create(self, values):
        if values.get('name', _('New')) == _('New'):
            values['name'] = self.env['ir.sequence'].next_by_code('uat.outcomes') or _('New')
        return super(uat_outcomes, self).create(values)