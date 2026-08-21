# Part of Odoo. See LICENSE file for full copyright and licensing details.
{
    'name': 'Israel - Accounting',
    'icon': '/account/static/description/l10n.png',
    'countries': ['il'],
    'version': '1.1',
    'category': 'Accounting/Localizations/Account Charts',
    'website': 'https://www.odoo.com/documentation/latest/applications/finance/fiscal_localizations.html',
    'depends': [
        'account',
    ],
    'auto_install': ['account'],
    'data': [
        'data/account_account_tag.xml',
        'data/account_tax_report_data.xml',
    ],
    'demo': [
        'demo/demo_company.xml',
    ],
    'author': 'Odoo S.A.',
    'license': 'LGPL-3',
}
