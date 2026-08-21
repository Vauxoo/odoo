# Part of Odoo. See LICENSE file for full copyright and licensing details.
{
    'name': "Gulf Cooperation Council WMS Accounting",
    'category': 'Accounting/Localizations',

    'depends': ['l10n_gcc_invoice', 'stock_account'],

    'data': [
        'views/report_invoice.xml',
    ],
    'auto_install': True,
    'author': 'Odoo S.A.',
    'license': 'LGPL-3',
}
