# Part of Odoo. See LICENSE file for full copyright and licensing details.
{
    'name': 'Serbia - Accounting',
    'website': 'https://www.odoo.com/documentation/latest/applications/finance/fiscal_localizations.html',
    'icon': '/account/static/description/l10n.png',
    'countries': ['rs'],
    'category': 'Accounting/Localizations/Account Charts',
    'author': 'Modoolar, Odoo S.A.',
    'depends': [
        'account',
    ],
    'auto_install': ['account'],
    'data': [
        'data/account_tax_report_data.xml',
        'data/menuitem_data.xml',
        'views/account_move.xml',
        'views/report_invoice.xml',
    ],
    'demo': [
        'demo/demo_company.xml',
    ],
    'license': 'LGPL-3',
}
