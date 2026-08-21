# Part of Odoo. See LICENSE file for full copyright and licensing details.
{
    'name': 'Vietnam - Accounting',
    'icon': '/account/static/description/l10n.png',
    'countries': ['vn'],
    'version': '2.0.3',
    'author': 'General Solutions',
    'website': 'https://www.odoo.com/documentation/latest/applications/finance/fiscal_localizations/vietnam.html',
    'category': 'Accounting/Localizations/Account Charts',
    'depends': [
        'account_qr_code_emv',
        'account',
    ],
    'auto_install': ['account'],
    'data': [
        'data/account_tax_report_data.xml',
        'views/account_move_views.xml',
        'views/res_bank_views.xml',
    ],
    'demo': [
        'demo/demo_company.xml',
    ],
    'license': 'LGPL-3',
}
