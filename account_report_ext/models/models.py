# -*- coding: utf-8 -*-

from odoo import models, fields, api, _

class Print(models.Model):
    _inherit = 'account.invoice'

    print_count = fields.Integer("Print Count", default=lambda x: _(-1))
    @api.onchange('print_count')
    def onchange_count(self):
        self.env.cr.execute('UPDATE account_invoice SET print_count = print_count+1 where print_count = print_count')

    # @api.multi()
    @api.depends('print_count')
    def create_report(self):
        self.onchange_count()
        self.printed()
        if self.print_count == 0:
            return self.env['report'].get_action(self, 'account_report_ext.account_invoice_report_edited_main')
        else:
            return self.env['report'].get_action(self, 'account_report_ext.account_invoice_report_reprint_main')
    
    is_printed = fields.Boolean("Is Printed?",  default=False)

    @api.model
    @api.onchange('print_count')
    def printed(self):
        if self.print_count != -1:
            printed = self.search([('is_printed', '=', False)])
            printed.write({'is_printed': True})
            return True

    active = fields.Boolean(default=True, help="The active field allows you to hide the category without removing it.")

    # class MV(models.Model):
    #     _name = "invoice.mv"
        
    #     _inherit = ['account.invoice']
        

        
        # _inherits = {'account.invoice': 'name'}
        
        

        # apple = fields.Char("Diwakar", size=20)
