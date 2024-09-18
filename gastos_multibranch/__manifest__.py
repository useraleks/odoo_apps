# -*- coding: utf-8 -*-
{
    'name': "Gastos de Terceros BRANCH",

    'summary': """
        ---> Separar gastos de terceros por branchs""",

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
    'depends': ['base', 'hr_expense'],

    # always loaded
    'data': [
        #'security/ir.model.access.csv',
        'views/res_users.xml',
        'views/hr_expense.xml',
        'views/hr_expense_sheet.xml',
        'views/hr_expense_tree.xml',
        'views/search_custom.xml',
    ],

    'installable': True,
    # only loaded in demonstration mode
    'demo': [
        'demo/demo.xml',
    ],
}