{
    'name': 'United Arab Emirates - Point of Sale',
    'category': 'Accounting/Localizations/Point of Sale',
    'author': 'Odoo S.A.',
    'license': 'LGPL-3',
    'depends': [
        'l10n_gcc_pos',
        'l10n_ae',
    ],
    'data': [
        'receipt/pos_order_receipt.xml',
    ],
    'assets': {
        'point_of_sale._assets_pos': [
            'l10n_ae_pos/static/src/**/*',
        ],
    },
    'auto_install': True,
}
