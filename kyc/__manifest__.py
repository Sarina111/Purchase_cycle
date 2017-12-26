# -*- coding: utf-8 -*-
{
    'name': "Know Your Clients",

    'summary': """
        Information about clients""",

    'description': """
       This module purpose is to keep the record about the clients.
    """,

    'author': "BI Solutions",
    'website': "http://bisolution.asia",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/master/odoo/addons/base/module/module_data.xml
    # for the full list
    'category': 'Know your client',
    # 'version': '0.1',

    # any module necessary for this one to work correctly
    'depends': ['mail','contacts','hr'],
	'application': True,
    'data': [
        'security/ir.model.access.csv',
        # 'security/kyc_access.xml',
        'views/views.xml',
        'views/templates.xml',
        'views/kanban_view.xml','reports/report.xml', 'data/kyc_data.xml',
        # 'views/wizard_view.xml',
    ],
    # only loaded in demonstration mode
    # 'demo': [
    #     'demo/demo.xml',
    # ],
}
