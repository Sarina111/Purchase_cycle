# -*- coding: utf-8 -*-

from odoo import models, fields, api

class hr_department_inherit(models.Model):
    _inherit = 'hr.department'
    # color = fields.Integer('Color Index')

    draft_fil = fields.Integer(compute='_compute_draft')
    to_be_approved_fil = fields.Integer(compute='_compute_to_be_approved')
    approved_fil = fields.Integer(compute='_compute_approved')
    rejected_fil = fields.Integer(compute='_compute_rejected')


    # draft######
    @api.multi
    def _compute_draft(self):
        amounts = self.env['purchase.request'].read_group([
            ('department', 'in', self.ids),
            ('state', '=', 'draft'),
        ], ['count_record', 'department'], ['department'])
        for rec in amounts:
            self.browse(rec['department'][0]).draft_fil = rec['count_record']

            # sent######

    @api.multi
    def _compute_to_be_approved(self):
        amounts = self.env['purchase.request'].read_group([
            ('department', 'in', self.ids),
            ('state', '=', 'to_be_approve'),
        ], ['count_record', 'department'], ['department'])
        for rec in amounts:
            self.browse(rec['department'][0]).to_be_approved_fil = rec['count_record']


            # to_approve######

    @api.multi
    def _compute_approved(self):
        amounts = self.env['purchase.request'].read_group([
            ('department', 'in', self.ids),
            ('state', '=', 'approved'),
        ], ['count_record', 'department'], ['department'])
        for rec in amounts:
            self.browse(rec['department'][0]).approved_fil = rec['count_record']


            # purchase######

    @api.multi
    def _compute_rejected(self):
        amounts = self.env['purchase.request'].read_group([
            ('department', 'in', self.ids),
            ('state', '=', 'rejected'),
        ], ['count_record', 'department'], ['department'])
        for rec in amounts:
            self.browse(rec['department'][0]).rejected_fil = rec['count_record']




