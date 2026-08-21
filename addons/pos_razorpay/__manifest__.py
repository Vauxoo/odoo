# Part of Odoo. See LICENSE file for full copyright and licensing details.
{
    'name': 'POS Razorpay',
    'category': 'Sales/Point of Sale',
    'sequence': 6,
    'summary': 'Integrate your POS with a Razorpay payment terminal',
    'data': [
        'views/pos_payment_method_views.xml',
    ],
    'depends': ['point_of_sale'],
    'assets': {
        'point_of_sale._assets_pos': [
            'pos_razorpay/static/src/**/*',
        ],
        'web.assets_tests': [
            'pos_razorpay/static/tests/tours/**/*',
        ],
        'web.assets_unit_tests': [
            'pos_razorpay/static/tests/unit/data/**/*'
        ],
    },
    'author': 'Odoo S.A.',
    'license': 'LGPL-3',
}
