# -*- coding: utf-8 -*-
{
    'name': "Bhada Chalan",

    'summary': """
        Bhadachalan application for Agni""",

    'description': """
        Bhadachalan of Agni
    """,

    'author': "BI Solutions",
    'website': "http://www.agni.com",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/master/odoo/addons/base/module/module_data.xml
    # for the full list
    'category': 'application',
    'version': '1.0',
    'application': True,

    # any module necessary for this one to work correctly
    'depends': ['base'],

    # always loaded
    'data': [
        # 'security/ir.model.access.csv',
        'views/bc_views.xml','data/se_data.xml'
        #'views/templates.xml',
    ],
    # only loaded in demonstration mode
    #'demo': [
     #   'demo/demo.xml',
   # ],
}
