# -*- coding: utf-8 -*-
{
    'name': "Verificacion De Empleados En Compras",

    'summary': """
        --> verica quien ha solicitado una compra""",

    'description': """

    """,

    'author': "Alexander.P",
    'website': "https://github.com/useraleks",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/15.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    'category': 'Uncategorized',
    'version': '0.1',

    # any module necessary for this one to work correctly
    'depends': ['base','hr','purchase','car_repair_industry'],

    # always loaded
    'data': [
        # 'security/ir.model.access.csv',
        'views/views.xml',
        'views/templates.xml',
        'views/purchase_order.xml',
    ],
    # only loaded in demonstration mode
    'demo': [
        'demo/demo.xml',
    ],
}
