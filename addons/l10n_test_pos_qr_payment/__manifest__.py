# Part of Odoo. See LICENSE file for full copyright and licensing details.

{
    'name': 'POS QR Tests',
    'category': 'Sales/Point of Sale',
    'sequence': 9876,
    'depends': [
        'point_of_sale',
        'account_qr_code_sepa',
        'l10n_be',
        'l10n_ch',
        'l10n_hk',
        'l10n_br',
    ],
    'assets': {
        'web.assets_tests': [
            'l10n_test_pos_qr_payment/static/tests/**/*',
        ],
    },
    'author': 'Odoo S.A.',
    'license': 'LGPL-3',
}
