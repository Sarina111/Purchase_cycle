# -*- coding: utf-8 -*-

from odoo import models, fields, api, _

class responsible(models.Model):
    _name = 'responsible'
    _description = 'Responsible Person'
    _rec_name ='person_name'
    person_name=fields.Char('Name')


class operationTask(models.Model):
    _name = 'operation'
    _description = 'Operations'
    _rec_name = 'operation_name'
    operation_name=fields.Char('Operation')


class teamTask(models.Model):
    _name = 'quality_alert_team'
    _description = 'Quality alert team'
    _rec_name='team_name'

    team_name=fields.Char('Team name')

    email=fields.Char('Email')

    @api.one
    def _get_count(self):
        alert_count = self.env['quality_alert'].search(
            [('stage', '=', 'Confirmed')])
        check_count = self.env['quality_check'].search(
            [('status', '=', 'open')])
        self.alert_count = len(alert_count)
        self.check_count = len(check_count)

    color = fields.Integer(string='Color Index')
    name = fields.Char(string="Name")
    alert_count = fields.Integer(compute='_get_count')
    check_count = fields.Integer(compute='_get_count')




class controlTask(models.Model):
    _name = 'quality_product'
    _description = 'Quality Management'
    _rec_name = 'sequence_id'
    title = fields.Char('Title')
    sequence_id= fields.Char('Reference', copy=False, readonly=True, default=lambda x:_('New'))
    product_name = fields.Many2one('product.product', 'Product')
    picking_type_id = fields.Integer('Picking_type_id')
    operation_name = fields.Many2one('operation','Operation')
    person_name = fields.Many2one('responsible', 'name')
    control_type = fields.Selection([('one', 'All Operations'), ('two', 'Randomly'),
                                               ('three', 'Periodically')], 'Control Type',default='one')

    test_type= fields.Selection([('one','Pass- Fail'), ('two','Measure'),
('three','Dummy'),('four','Take a Picture')],'State',default='one')
    team_name= fields.Many2one('quality_alert_team','Team')
    user_id = fields.Integer('User_id')
    notes= fields.Text('Notes')
    instruction = fields.Text('Instructions')
    reason= fields.Text('Reason')
    message = fields.Text('Message If Failure')
    measure_frequency_unit_value= fields.Integer('measure_frequency_unit_value')
    measure_frequency_unit = fields.Selection([('one', 'Days'), ('two', 'Weeks'),
                                               ('three', 'Months')], 'Frequency Unit',default='one')
    norm =fields.Float('Norm')
    norm_unit = fields.Char('Norm_unit',default='mm')
    tolerance_min= fields.Float('Tolerance_min')
    check=fields.Boolean('Checked?')
    #active=fields.Boolean([('0','active'), ('1','inactive')])
    tolerance_max= fields.Float()


    @api.model
    def create(self, values):
        if values.get('sequence_id', _('New')) == _('New'):
            values['sequence_id'] = self.env['ir.sequence'].next_by_code('bharpai.bharpai') or _('New')
        return super(controlTask, self).create(values)


class qcheckTask(models.Model):
    _name = 'quality_check'
    _rec_name = 'product_name'
    _description = 'Quality Check'
    team_name= fields.Many2one('quality_alert_team','Team')
    sequence_id = fields.Char('Reference', copy=False, readonly=True, default=lambda x: _('New'))

    product_name = fields.Many2one('product.product', 'Product',required='True')
    operation=fields.Selection([('draft','New'), ('open','Started'),
('done','Closed')],String="Operation")
    notes= fields.Text('Notes')
    point_id= fields.Many2one('quality_product','title',String="Control Point")
    product_id=fields.Many2one('quality_product','Product')
    status=fields.Selection([('draft','Todo'), ('open','passed'),
('done','Failed')],'Status')
    check_date=fields.Datetime('Checked Date')
    check_by=fields.Many2one('responsible',String="Checked by")

    @api.model
    def create(self, values):
        if values.get('sequence_id', _('New')) == _('New'):
            values['sequence_id'] = self.env['ir.sequence'].next_by_code('bharpai.bharpai1') or _('New')
        return super(qcheckTask, self).create(values)

    @api.one
    def do_Pass(self):
        for task in self:
         task.write({'status': 'open'})

         return True

    @api.one
    def do_Fail(self):
        self.write({'status': 'done'})


class qmgntTask2(models.Model):
    _name = 'quality_tag'
    _description ='Quality Tag'
    tag_ids = fields.Integer('Tag Ids')
    name= fields.Char('Tag name')
class qmgntTask3(models.Model):
    _name = 'quality_alert_stages'
    _description = 'Quality Alert Stages'
    name=fields.Char('Stage Name')
    folded= fields.Boolean('Folded')
    sequence=fields.Integer('Sequence')
    done=fields.Boolean('Done?')


class reasonTask(models.Model):
    _name = 'quality_reason'
    _description = 'Quality Reason'
    reason_id= fields.Integer('Reason Id')
    name=fields.Char('reason name')





class qmgntTask1(models.Model):

    _name= 'quality_alert'
    _description ='Quality Alert'

    sequence_id = fields.Char('Reference', copy=False, readonly=True, default=lambda x: _('New'))

    description= fields.Text('Description')
    action_corrective= fields.Text('Action_corrective')
    action_preventive = fields.Text('Action_preventive')
    partner_id =fields.Char('Partner_id')
    date_assign=fields.Date('Date Assign')
    stage= fields.Many2one('quality_alert_stages', 'Stage')
    quality_check=fields.Boolean('Quality Check', default=False)
    person_name=fields.Many2one('responsible','name')

    priority = fields.Selection(
        [('0', 'Low'), ('1', 'Normal'), ('2', 'Medium'),('3', 'High')],
        'Priority')
    reason_id =fields.Many2one('quality_reason', 'reason_id')
    tag_ids =fields.Many2one('quality_tag', 'tag_ids')
   # user_id=fields.Integer('User Id')
    team_id=fields.Many2one('quality_alert_team','team_id')
    product_name = fields.Many2one('product.product','Product')

    @api.model
    def create(self, values):
        if values.get('sequence_id', _('New')) == _('New'):
            values['sequence_id'] = self.env['ir.sequence'].next_by_code('bharpai.bharpai2') or _('New')
        return super(qmgntTask1, self).create(values)


