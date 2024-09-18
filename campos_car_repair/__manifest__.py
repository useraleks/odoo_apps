# -*- coding: utf-8 -*-
{
    'name': "Car repair cosas adicionales",

    'summary': """
        ---> Car repair cosas adicionales""",

    'description': """
    """,

    'author': "Alexander P.",
    'website': "https://github.com/useraleks",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/15.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    'category': '',
    'version': '0.1',

    # any module necessary for this one to work correctly
    'depends': ['base', 'car_repair_industry'],

    # always loaded
    'data': [
        'security/groups.xml',
        'views/views.xml',
    ],

    'installable': True,
    # only loaded in demonstration mode
    'demo': [
        'demo/demo.xml',
    ],
}