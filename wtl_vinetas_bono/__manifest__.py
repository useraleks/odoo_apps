# -*- coding: utf-8 -*-
{
    'name': "Viñetas Bono",
    'summary': """""",
    'description': """
        """,
    'author': "WitLink[Alexander P.]",
    'version': '16.1',
    'website': "",
    'license': 'LGPL-3',
    'category': 'sale',
    'depends': ['base', 'stock', 'account', 'product', 'contacts', 'sale', 'web', 'account_accountant'],
    'data': [
        #'data/res_lang.xml',
        'security/groups.xml',
        'security/ir.model.access.csv',
        
        'wizard/print_vinetas_bono_wizard.xml',
        'wizard/re_print_vinetas_bono_wizard.xml',
        'wizard/cancel_vinetas_bono_wizard.xml',
        'wizard/authorize_vinetas_bono_wizard.xml',
        'report/product_label_templates_vtn.xml',
        'report/product_label_reports_vtn.xml',
        'data/data.xml',
        'views/settings_accounting.xml',
        'views/res_company.xml',
        'views/product.xml',
        'views/res_partner.xml',
        'views/product_pricelist.xml',
        'views/sale_order.xml',
        'views/vineta_bono_view.xml',
        'views/menu_items.xml',
        'views/stock_picking.xml',
        'views/vineta_payment.xml',
        'views/account_move.xml',
    ],
    'installable': True,
    'application': True,
}