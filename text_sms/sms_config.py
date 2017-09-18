from . import models, fields, api

class SmsSetting(models.TransientModel):
    _name = 'sms.config.settings'
    _description = 'SMS description '
    sms_sender = fields.Char(default_model='smsnp.send', string="Sender")