{
    'name': "Italy - Stock DDT",
    'category': 'Accounting/Localizations/EDI',
    'version': '0.1',
    'depends': ['l10n_it_edi', 'stock_delivery', 'stock_account'],
    'data': [
        'report/l10n_it_ddt_report.xml',
        'views/stock_picking_views.xml',
        'views/account_invoice_views.xml',
        'data/l10n_it_ddt_template.xml',
    ],
    'auto_install': True,
    'post_init_hook': '_create_picking_seq',
    'author': 'Odoo S.A.',
    'license': 'LGPL-3',
}
