# Part of Odoo. See LICENSE file for full copyright and licensing details.
{
    'name': 'Argentinean - Point of Sale with AR Doc',
    'category': 'Accounting/Localizations/Point of Sale',
    'depends': [
        'l10n_ar',
        'point_of_sale',
    ],
    'data': [
        'views/templates.xml',
    ],
    'assets': {
        'point_of_sale._assets_pos': [
            'l10n_ar_pos/static/src/**/*'
        ],
        'web.assets_tests': [
            'l10n_ar_pos/static/tests/tours/**/*',
        ],
    },
    'auto_install': True,
    'author': 'Odoo S.A.',
    'license': 'LGPL-3',
}
