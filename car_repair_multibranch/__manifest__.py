# -*- coding: utf-8 -*-
{
    'name': "Branch para taller",

    'summary': """
        ---> Car repair branch""",

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
        'security/ir.model.access.csv',
        'data/data.xml',
        'views/views.xml',
        'views/fleet_repair.xml',
        'views/fleet_vehicle.xml',
        'views/fleet_diagnose.xml',
        'views/res_company.xml',
        'views/sale_order.xml',
        'views/hr_employee.xml',
        'views/checklists_chasis.xml',
        'views/checklists_documental.xml',
        'views/checklists_piloto.xml',
        'views/checklists_exterior.xml',
        'views/checklists_interior.xml',
        'views/checklists_complementos.xml',
        'views/checklists_tanque.xml',
        'views/fleet_workorder.xml',
        'views/menu_items.xml',
        'views/fleet_vehicle_log.xml',
        'views/taller_listview.xml',
    ],

    'installable': True,
    # only loaded in demonstration mode
    'demo': [
        'demo/demo.xml',
    ],
}