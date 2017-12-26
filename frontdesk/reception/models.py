from odoo import models,fields,api

class IncomingEmail(models.Model):
    _name = 'email_inc'

    email_for = fields.Char(required="True",string="Receipent")
    received_date = fields.Date(string="Received date")
    subject = fields.Text(required="True",string="Subject")
    description = fields.Text(string="Description")
    # action = fields.Selection("")

class OutgoingEmail(models.Model):
    _name = "email_out"

    email_by = fields.Char(required="True",string="Sender")
    sent_date = fields.Date(string="Sent date")
    subject = fields.Text(required="True",string="Subject")
    description = fields.Text(string="Description")

class IncLetters(models.Model):
    _name = "letters_inc"

    ref_no = fields.Integer(required="True",string="Ref.no:")
    received_date = fields.Date(string="Received date")
    letter_for = fields.Char(required="True",string="Letter for")
    subject = fields.Text(required="True",string="Subject")
    description = fields.Text(string="Description")

class OutLetters(models.Model):
    _name = "letters_out"

    ref_no = fields.Integer(required="True",string="Ref.no:")
    sent_date = fields.Date(string="Sent date")
    letter_by = fields.Char(required="True",string="Letter by")
    subject = fields.Text(required="True",string="Subject")
    description = fields.Text(string="Description")

class Notes(models.Model):
    _inherit = "note.note"

    created_by = fields.Char(string="Created by")

class IncPhones(models.Model):

    _name = "phone_inc"

    phn_no = fields.Integer(required="True",string="Phn.no:")
    received_date = fields.Datetime(string="Received at:")
    subject = fields.Text(required="True",string="Subject")
    description = fields.Text(string="Description")
    
class OutPhones(models.Model):

    _name = "phone_out"

    phn_no = fields.Integer(required="True",string="Phn.no:")
    called_date = fields.Datetime(string="Called at:")
    subject = fields.Text(required="True",string="Subject")
    description = fields.Text(string="Description")


# class MailComposer(models.TransientModel):
#     _name = "reception.mail.template"
#     _inherit = 'mail.compose.message'
#     _description = 'Email composition wizard inherited'


#     test_field = fields.Char('Test Field')
#     subject1 = fields.Char('Subjecttttttttttttttttt')
 

class TemplateComposer(models.Model):
    
    _name = "templates.frontdesk"
    _rec_name = "template_name"
    
    
    template_name = fields.Char(string="Template name")
    receipents = fields.Many2one('res.partner',string="Receipent")
    template_save = fields.Many2one("template.saved",string="Use template")
    subject = fields.Char(string="Subject",related = "template_save.subject")
    sender = fields.Many2one('res.partner',string="Sender")
    
    # use_template = fields.Many2one("",string="Use Template")
    desc = fields.Html(string="Description",related = "template_save.desc")
    

    
    @api.multi
    def data_flow(self):
        inv_obj = self.env['template.saved']

        for rec in self:
            var = inv_obj.create({
                'template_name': rec.template_name,
                'subject': rec.subject,
                'desc': rec.desc,

            })
        return var

class TemplateSaved(models.Model):

    _name = "template.saved"
    _rec_name = "template_name"

    template_name = fields.Char(string="Template name")
    subject = fields.Char(string="Subject")
    desc = fields.Html(string="Description")


    

    