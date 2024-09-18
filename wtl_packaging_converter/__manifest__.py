# -*- coding: utf-8 -*-
{
    'name': "Conversor de empaquetado",
    'summary': """""",
    'description': """
        """,
    'author': "WitLink[Alexander P.]",
    'version': '16.1',
    'website': "",
    'license': 'LGPL-3',
    'category': 'purchase',
    'depends': ['base', 'point_of_sale','stock', 'sale', 'product', 'purchase'],
    'data': [
        #'data/res_lang.xml',
        #'security/groups.xml',
        #'security/ir.model.access.csv',
        
        'views/purchase_order.xml',
        'views/product.xml',
        'views/stock_quant.xml',
        'views/sale_order.xml',
        'views/stock_lot.xml',
        'views/stock_move_line.xml',
        'views/stock_warehouse_orderpoint.xml',
        'views/product_pricelist.xml',
        'views/uom_uom.xml',
        'views/stock_valuation_layer.xml',
        #'views/forecasted_header.xml',
    ],
    'assets':{
        'point_of_sale.assets':[
            "wtl_packaging_converter/static/src/xml/ProductInfoPopup.xml",
        ]
    },
    'installable': True,
    'application': True,
}