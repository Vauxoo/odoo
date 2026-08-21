# Part of Odoo. See LICENSE file for full copyright and licensing details.
{
    'name': 'Mongolia - Accounting',
    'website': 'https://www.odoo.com/documentation/latest/applications/finance/fiscal_localizations.html',
    'version': '1.1',
    'icon': '/account/static/description/l10n.png',
    'countries': ['mn'],
    'category': 'Accounting/Localizations/Account Charts',
    'author': 'BumanIT LLC, Odoo S.A.',
    'depends': [
        'account',
    ],
    'auto_install': ['account'],
    'data': [
        'data/account.account.tag.csv',
        'data/vat_report.xml',
    ],
    'demo': [
        'demo/demo_company.xml',
    ],
    'license': 'LGPL-3',
}
