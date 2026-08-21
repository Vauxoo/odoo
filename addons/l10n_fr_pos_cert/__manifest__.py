# Part of Odoo. See LICENSE file for full copyright and licensing details.

{
    'name': 'France - VAT Anti-Fraud Certification for Point of Sale (CGI 286 I-3 bis)',
    'version': '1.1',
    'category': 'Accounting/Localizations/Point of Sale',
    'depends': ['l10n_fr_account', 'point_of_sale'],
    'auto_install': True,
    'data': [
        'views/pos_views.xml',
        'views/account_sale_closure.xml',
        'views/pos_inalterability_menuitem.xml',
        'views/res_config_settings_views.xml',
        'report/pos_hash_integrity.xml',
        'data/account_sale_closure_cron.xml',
        'receipt/pos_order_receipt.xml',
        'security/ir.access.csv',
    ],
    'post_init_hook': '_setup_inalterability',
    'assets': {
        'web.assets_unit_tests': [
            'l10n_fr_pos_cert/static/tests/unit/**/*',
        ],
        'point_of_sale._assets_pos': [
            'l10n_fr_pos_cert/static/src/**/*',
        ],
        'web.assets_tests': [
            'l10n_fr_pos_cert/static/tests/tours/**/*',
        ],
    },
    'author': 'Odoo S.A.',
    'license': 'LGPL-3',
}
