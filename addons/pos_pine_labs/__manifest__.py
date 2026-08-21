{
    'name': 'POS Pine Labs',
    'category': 'Sales/Point of Sale',
    'sequence': 6,
    'summary': 'Integrate your POS with Pine Labs payment terminals',
    'data': [
        'views/pos_payment_views.xml',
        'views/pos_payment_method_views.xml',
    ],
    'depends': ['point_of_sale'],
    'assets': {
        'point_of_sale._assets_pos': [
            'pos_pine_labs/static/src/**/*',
        ],
        'web.assets_unit_tests': [
            'pos_pine_labs/static/tests/unit/data/**/*',
        ],
    },
    'author': 'Odoo S.A.',
    'license': 'LGPL-3',
}
