# -*- coding: utf-8 -*-

from odoo import models, fields, api

class uat_modules(models.Model):
    _name = 'uat.modules'
    module_name=fields.Char(string='Module Name')
    version=fields.Float(string='Version')
    
    module_id=fields.One2many('uat.class','module_id')

class uat_class(models.Model):
    _name = 'uat.class'
    class_name=fields.Char(string='Class Name')
    version=fields.Float(string='Version')
    module_id=fields.Many2one('uat.modules')
   
    class_id=fields.One2many('uat.testcase','test_id')
    
class uat_testcase(models.Model):
    _name = 'uat.testcase'
    statement=fields.Char(string='Statement')
    expected_result=fields.Char(string='Expected Result')
    actual_result=fields.Char(string='Actual Result')
   
    test_id=fields.Many2one('uat.test')
    class_id=fields.Many2one('uat.class')
    case_id=fields.One2many('uat.outcomes','case_id')


class uat_users(models.Model):
    _name = 'uat.users'
    name=fields.Char(string='Name')
    organization=fields.Text(string='Organization')


class uat_test(models.Model):
    _name = 'uat.test'
    test_date=fields.Date(string='Date')
    test_project=fields.Char(string='Test Project')
    test_version=fields.Float(string='Test Version')

    test_id=fields.One2many('uat.testcase','test_id')

class uat_outcomes(models.Model):
    _name = 'uat.outcomes'
    test_result=fields.Boolean(string='Test Result')
    test_remarks=fields.Text(string='Test Remarks')
    
    case_id=fields.Many2one('uat.testcase')
