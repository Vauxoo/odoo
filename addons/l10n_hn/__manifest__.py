# Part of Odoo. See LICENSE file for full copyright and licensing details.
{
    'name': 'Honduras - Accounting',
    'icon': '/account/static/description/l10n.png',
    'countries': ['hn'],
    'version': '0.2',
    'category': 'Accounting/Localizations/Account Charts',
    'author': 'Salvatore Josue Trimarchi Pinto',
    'website': 'https://www.odoo.com/documentation/latest/applications/finance/fiscal_localizations.html',
    'depends': [
        'base',
        'account',
    ],
    'auto_install': ['account'],
    'demo': [
        'demo/demo_company.xml',
    ],
    'license': 'LGPL-3',
}
