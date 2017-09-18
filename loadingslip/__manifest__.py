# -*- coding: utf-8 -*-
{
    'name': "Dispatch",

    # 'summary': """
    #     Short (1 phrase/line) summary of the module's purpose, used as
    #     subtitle on modules listing or apps.openerp.com""",
    #
    # 'description': """
    #     Long description of module's purpose
    # """,

    'author': "BI solution",
    # 'website': "http://www.yourcompany.com",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/master/odoo/addons/base/module/module_data.xml
    # for the full list
    'category': 'Uncategorized',
    'version': '0.1',

    # any module necessary for this one to work correctly
    'depends': ['base','sale','contacts','sales_eet_agni',],

    # always loaded
    'data': [
        # 'security/ir.model.access.csv',
        'views/views.xml',
        'views/templates.xml','data/se_data.xml','reports/loadingslip_report.xml',
        'reports/report_gatepass.xml','reports/report_bhadachalan_sales.xml'
    ],
    # only loaded in demonstration mode
    'demo': [
        'demo/demo.xml',
    ],
}