# -*- coding: utf-8 -*-
{
    'name': "Reporteria con Wizard",

    'summary': "--> Reporteria General",

    'author': "Alexander P., WitLinkGT",
    'website': "https://witlinkgt.com/",
    'category': 'reporteria',
    'version': '0.1',

    'depends': ['base', 'sale_renting', 'fleet_customization', 'fields_for_reporting', 'report_xlsx'],

    'data': [
        'security/ir.model.access.csv',
        'wizard/wiz_view.xml',
        'views/formatodepapel.xml',
        'views/reports_action.xml',
        'views/cuadro_despachos_template.xml',
    ],
}
