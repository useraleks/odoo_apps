# -*- coding: utf-8 -*-
{
    'name': "bill_report",

    'summary': """
        ---> reporte de factura customizado""",

    'description': """
    """,

    'author': "Alexander",
    'website': "https://witlinkgt.com/",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/15.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    'category': 'Uncategorized',
    'version': '0.1',

    # any module necessary for this one to work correctly
    'depends': ['base', 'account'],

    # always loaded
    'data': [
        # 'security/ir.model.access.csv',
        'views/formatodepapel.xml',
        'views/bill_action.xml',
        'views/bill_template.xml',
        'views/bill_template_gastos.xml',
        'views/account_move.xml',
        
    ],
    # only loaded in demonstration mode
    'demo': [
        'demo/demo.xml',
    ],
}
