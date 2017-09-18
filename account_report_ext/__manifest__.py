# -*- coding: utf-8 -*-
{
    'name': "Account Report Ext",

    'summary': """
        Reprint Numbering""",

    'description': """
        Account invoice can be printed multiple times but with title showing Reprint and iterated number.
    """,

    'author': "BI Solutions",
    'website': "http://www.bisolutions.asia",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/master/odoo/addons/base/module/module_data.xml
    # for the full list
    'category': 'applications',
    'version': '1',

    # any module necessary for this one to work correctly
    'depends': ['base', 'account', 'report_xml','sales_ext_invoice','sale_discount_total','sales_eet_agni'],

    # always loaded
    'data': [
        # 'security/ir.model.access.csv',
        'views/views.xml',
	'material_view_report.xml',
	'sale_register.xml','invoice_agni.xml'
        # 'views/templates.xml',
    ],
    # only loaded in demonstration mode
    # 'demo': [
    #     'demo/demo.xml',
    # ],
}
