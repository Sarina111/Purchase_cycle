# -*- coding: utf-8 -*-
from odoo import models, fields, api
import requests
from pprint import pprint


class SendSms(models.Model):
    _name = 'smsnp.send1'
    # token = fields.Text(required=True, string='Token')
    token = fields.Selection([('4symSqCEVvG1zIEdWFcz', '4symSqCEVvG1zIEdWFcz')],
                             default='4symSqCEVvG1zIEdWFcz', required=True, string='Token')
    text_from = fields.Selection([('InfoSMS', 'Info SMS'),('AgniCement','Agni Cement')],
                     default='InfoSMS', required=True, string='Text From')
    customer = fields.Many2one('res.partner', string='Customer')
    # text_from = fields.Char(realted='customer.mobile', string='Text From')
    # tag_ids = fields.Many2many('note.tag', 'note_tags_rel', 'note_id', 'tag_id', string='Tags')
    # text_to = fields.Char(related='customer.mobile', required=True, string='Text To')
    text_to = fields.Char()
    sms_template = fields.Many2one('smsnp.template1', string='SMS Template')
    # customer = fields.Many2one('res.users', string='Customer')
    # text_from = fields.Char(realted='customer.mobile', string='Text From')

    text_msg = fields.Char(required=True, string='Text message')
    sale_name = fields.Char(string='Sale Order No.')
    invoice_name = fields.Char(string='Invoice No.')
    text_msg = fields.Text(related='sms_template.template_sms_body', required=True, string='Text message',
                           default="Dear Mr. Manager. Please approve the sale order for the recent quotation items.")
    # text_msg = fields.Text(required=True, string='Text message')
    # token = fields.Char(value='4symSqCEVvG1zIEdWFcz')
    # text_from = fields.Char(value='InfoSMS')
    state = fields.Selection([('waiting_for_approval','Waiting for approval'),
                              ('approved','Approved')
                              ])



    # @api.depends('token', 'text_from', 'text_to', 'text_msg')
    @api.depends('text_to', 'text_msg')
    def post_msg(self):
        # import pdb;
        # pdb.set_trace()
        # pprint('token')
        # pprint('text_from')
        # pprint('text_to')
        r = requests.get(
            "http://api.sparrowsms.com/v2/sms",
            params={
                'token': '4symSqCEVvG1zIEdWFcz',
                'from': 'InfoSMS',
                # 'to': self.user_id.mobile,
                # 'to': self.user_id.mobile,
                'to': self.text_to,
                # 'text': 'This is test message'
                'text': self.text_msg
            }
        )
        self.change_state()
        return r

    @api.multi
    def change_state(self):
        # self.ensure_one()
        self.write({'state':'approved'})




        # status_code = r.status_code
        # response = r.text
        # response_json = r.json()

    # @api.one
    # def post_msg(self):
    #     self._post_msg()

# TASK DONE BY SHSAHI #
#######################

# SMS template
class SmsTemplate(models.Model):
    _name = 'smsnp.template1'
    _rec_name = 'template_name'
    template_name = fields.Char(string='Template Name', required=True)
    template_sms_body = fields.Text(string='Template SMS Body', required=True)


# class SMSSettingWizard(models.TransientModel):
#     _name = 'sms.wizard1'
# #     _description = 'SMS setting wizard'
# #     wiz_token = fields.Char('Token Wiz')
# #     wiz_sms = fields.Many2one('smsnp.send', 'wiz_sms_rel')
#     wiz_token = fields.Char(required=True, string='Token')
# #     # default = '4symSqCEVvG1zIEdWFcz'
#     wizard_text_from = fields.Char(default='InfoSMS', required=True, string='Text From')
#     verification_needed = fields.Boolean(string="Verification Needed?")
#
#     @api.one
#     def sms_flow(self):
#         wiz_

# transient model new try with res.config.setting inheritance from
# http://ludwiktrammer.github.io/odoo/custom-settings-odoo.html

class SMSSetting(models.TransientModel):
    _inherit = 'res.config.settings'
    _name = 'sms.config.settings'
    sms_token = fields.Char()
    sms_from = fields.Char()

    # token = fields.Char(default_model='smsnp.send1')
    # text_from = fields.Char(default_model='smsnp.send1')



    # @api.model
    # def get_default_token_values(self, fields):
    #     """
    #         Method argument "fields" is a list of names
    #         of all available fields.
    #         """
    #     sms = self.env['smsnp.send1']
    #     return {
    #         'sms_token': sms.token,
    #         'sms_from': sms.text_from,
    #     }


    # using api model
    # other setting

    def set_sms_values(self):
        """
        Method argument "fields" is a list of names
            of all available fields.
        """
        sms = self.env['smsnp.send1']
        sms.update({
            'token': self.sms_token,
            'text_from': self.sms_from
        })

        # import pdb; pdb.set_trace()
        # sms = self.env['smsnp.send1']
        # return {
        #     'token': self.sms_token,
        #     'text_from': self.sms_from
            # 'sms_token': sms.token,
            # 'sms_from': sms.text_from
        # }

    # using api model
    # def set_sms_values(self, fields):
    #
    # sms =



    # using api one
    # @api.one
    # def set_sms_values(self):
    #     sms = self.env['smsnp.send1']
    #     sms.token = self.sms_token
    #     sms.text_from = self.sms_from
