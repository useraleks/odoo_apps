# -*- coding: utf-8 -*-
{
    'name': "Recepcion de vehiculos",

    'summary': """
        ---> Modulo para la recepcion de vehiculos""",

    'description': """
    """,

    'author': "Alexander P.",
    'website': "https://github.com/useraleks",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/15.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    'category': 'fleet',
    'version': '0.1',

    # any module necessary for this one to work correctly
    'depends': ['base', 'fleet', 'car_repair_multibranch'],

    # always loaded
    'data': [
        'security/ir.model.access.csv',
        'report/fleet_repair_receipt.xml',
        'report/vehicle_reception_menu.xml',
        'report/vehicle_reception_checklist_view.xml',
        'report/vehicle_reception_checklist_menu.xml',
        'data/data.xml',
        'views/vehicle_reception.xml',
        'views/checklist_log.xml',
        'views/menu_items.xml',
        'views/vehicle_reception_line.xml',
        'views/fleet_vehicle.xml',
        'views/fleet_vehicle_odometer.xml',
        'views/fleet_repair.xml',
    ],

    'installable': True,
}