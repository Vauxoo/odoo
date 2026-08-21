# Part of Odoo. See LICENSE file for full copyright and licensing details.

{
    'name': 'PoS DPO Pay',
    'category': 'Sales/Point of Sale',
    'sequence': 6,
    'summary': 'Integrate your POS with DPO payment terminal.',
    'data': [
        'views/pos_payment_method_views.xml',
        'views/pos_payment_views.xml',
    ],
    'depends': ['point_of_sale'],
    'assets': {
        'point_of_sale._assets_pos': [
            'pos_dpopay/static/src/**/*',
        ],
    },
    'author': 'Odoo S.A.',
    'license': 'LGPL-3',
}
