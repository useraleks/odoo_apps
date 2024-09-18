# -*- coding: utf-8 -*-
{
    'name': "Mostrar PopUp POS",
    'summary': "",
    'description':"WitLink Apps",
    'author': "Alexander P., WitLink",
    'website': "https://witlinkgt.com/",
    'category': 'point_of_sale',
    'version': '0.1',
    'license': 'LGPL-3',
    'depends': ['base','point_of_sale', 'product'],
    'data': [
        'views/product.xml'
    ],
    'assets':{
        'point_of_sale.assets':[
            "show_popup_prescription/static/src/js/customize_button.js",
            "show_popup_prescription/static/src/xml/hide_expected.xml",
            "show_popup_prescription/static/src/xml/show_qty.xml",
        ]
    },
    'installable': True,
    'application': True,
    'auto_install': False
}
