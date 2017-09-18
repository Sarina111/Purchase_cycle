# -*- coding: utf-8 -*-
from odoo import models, fields, api
import requests

# class SmsSetting(models.Model):
#     _name = 'smsnp.setting'
#     _description = 'Send sms'
#     url = fields.Char(required=True,string='URL')
#     keyword = fields.Char('Keyword')
#     shortcode = fields.Char('Shortcode')
#     reply = fields.Text('Text Message')

class SendSms(models.Model):
    _name = 'smsnp.send'
    # token = fields.Text(required=True, string='Token')
    token = fields.Selection([('4symSqCEVvG1zIEdWFcz', '4symSqCEVvG1zIEdWFcz')],
                             default='4symSqCEVvG1zIEdWFcz', required=True, string='Token')
    text_from = fields.Selection([('InfoSMS', 'Info SMS'),('AgniCement','Agni Cement')],
                     default='InfoSMS', required=True, string='Text From')
    customer = fields.Many2one('res.partner', string='Customer')
    # text_from = fields.Char(realted='customer.mobile', string='Text From')
    # tag_ids = fields.Many2many('note.tag', 'note_tags_rel', 'note_id', 'tag_id', string='Tags')
    text_to = fields.Char(related='customer.mobile', required=True, string='Text To')
    sms_template = fields.Many2one('smsnp.template', string='SMS Template')
    text_msg = fields.Text(related='sms_template.template_sms_body', required=True, string='Text message')
    # text_msg = fields.Text(required=True, string='Text message')

    @api.depends('token', 'text_from', 'text_to', 'text_msg')
    def post_msg(self):
        r = requests.get(
            "http://api.sparrowsms.com/v2/sms",
            params={
                'token': self.token,
                'from': self.text_from,
                'to': self.text_to,
                'text': self.text_msg
            }
        )
        return r
        # status_code = r.status_code
        # response = r.text
        # response_json = r.json()

    # @api.one
    # def post_msg(self):
    #     self._post_msg()


# class Report(models.Model):
#     _name = 'report.sms'
#     symbol_no = fields.Integer(string='SN')
#     text_text = fields.Char(string='Text')
#
#     @api.multi
#     def sms_report(self):
#         # self.filtered(lambda s: s.state == 'draft').write({'state': 'sent'})
#         return self.env['report.sms'].get_action(self, 'sms_api.report_sms_agni')

    # @http.route(['/shop/print'], type='http', auth="public", website=True)
    # def print_saleorder(self):
    #     sale_order_id = request.session.get('sale_last_order_id')
    #     if sale_order_id:
    #         pdf = request.env['report'].sudo().get_pdf([sale_order_id], 'sale.report_saleorder', data=None)
    #         pdfhttpheaders = [('Content-Type', 'application/pdf'), ('Content-Length', len(pdf))]
    #         return request.make_response(pdf, headers=pdfhttpheaders)
    #     else:
    #         return request.redirect('/shop')



    # configuration setting try

# class MySetting(models.TransientModel):
#     _inherit = 'res.partner'
#     _name = 'your.config.settings'
#
#     default_name = fields.Char(default_model='your.other.model')
#
#     group_kill = fields.Boolean(
#         group = 'your.secret_agent',
#         implied_group = 'your.licence_to_kill'
#     )
#
#     module_spies = fields.Boolean()




# TASK DONE BY SHSAHI #
#######################

# SMS template
class SmsTemplate(models.Model):
    _name = 'smsnp.template'

    template_name = fields.Char(string='Template Name', required=True)
    template_sms_body = fields.Text(string='Template SMS Body', required=True)
        


# Transient Model for Setting Wizard
# class SMSSettingWizard(models.TransientModel):
#     _name = 'sms.wizard1'
#     _description = 'SMS setting wizard'
#     wiz_token = fields.Char('Token Wiz')
#     wiz_sms = fields.Many2one('smsnp.send', 'wiz_sms_rel')
#     wiz_token = fields.Char(required=True, string='Token')
#     # default = '4symSqCEVvG1zIEdWFcz'
#     wizard_text_from = fields.Char(default='InfoSMS', required=True, string='Text From')
#     verification_needed = fields.Boolean(string="Verification Needed?")


