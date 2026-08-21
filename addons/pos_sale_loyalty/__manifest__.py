# Part of Odoo. See LICENSE file for full copyright and licensing details.


{
    'name': 'POS - Sales Loyality',
    'category': 'Sales/Point of Sale',
    'sequence': 6,
    'summary': 'Link module between pos_sale and pos_loyalty',
    'depends': ['pos_sale', 'pos_loyalty'],
    'auto_install': True,
    'assets': {
        'point_of_sale._assets_pos': [
            'pos_sale_loyalty/static/src/**/*',
        ],
        'web.assets_tests': [
            'pos_sale_loyalty/static/tests/tours/**/*',
        ],
    },
    'author': 'Odoo S.A.',
    'license': 'LGPL-3',
}
