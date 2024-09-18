{
    'name': 'REPORTE DE REGISTRO DE CONTROL DE INVENTARIO',
    'author': 'Alexander P., WitLink',
    'version': '16.0.0.0',
    'category': 'Reports',
    'summary': 'REPORTE DE REGISTRO DE CONTROL DE INVENTARIO, INVENTARIO',
    'depends': ['stock', 'base', 'stock_account', 'contacts'],
    'data': [
        'security/ir.model.access.csv',
        'wizard/wiz_view.xml',
        'views/stock_valuation_layer.xml',
        'views/res_partner.xml',
        'reports/paperformat.xml',
        'reports/reports_action.xml',
        'reports/control_de_inventario.xml',
    ],
    'installable': True,
    'application': True,
    'license': 'LGPL-3',
    'assets': {
    'web.report_assets_common': [
        'wtl_reporte_control_de_inventario/static/src/scss/style.scss',
    ],
}
}