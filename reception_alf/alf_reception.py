import httplib2
import functools

# Set system CA Certificates based SSL Certificate Validation by python code
httplib2.Http = functools.partial(
    httplib2.Http,
    ca_certs="/etc/ssl/certs/ca-certificates.crt"
)



from odoo import models
from odoo.addons.cmis_field import fields


class IncEmail(models.Model):
    _inherit = 'email_inc'
    cmis_folder = fields.CmisFolder()

class OutEmail(models.Model):
    _inherit = 'email_out'
    cmis_folder = fields.CmisFolder()

class IncLetters(models.Model):
    _inherit = 'letters_inc'
    cmis_folder = fields.CmisFolder()

class OutLetters(models.Model):
    _inherit = 'letters_out'
    cmis_folder = fields.CmisFolder()

class IncPhone(models.Model):
    _inherit = 'phone_inc'
    cmis_folder = fields.CmisFolder()

class OutPhone(models.Model):
    _inherit = 'phone_out'
    cmis_folder = fields.CmisFolder()

class Alfnotes(models.Model):
    _inherit = "note.note"
    cmis_folder = fields.CmisFolder()



