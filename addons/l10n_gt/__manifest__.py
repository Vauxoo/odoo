# Part of Odoo. See LICENSE file for full copyright and licensing details.
{
    'name': 'Guatemala - Accounting',
    'icon': '/account/static/description/l10n.png',
    'countries': ['gt'],
    'version': '3.0',
    'category': 'Accounting/Localizations/Account Charts',
    'author': 'José Rodrigo Fernández Menegazzo',
    'website': 'https://www.odoo.com/documentation/latest/applications/finance/fiscal_localizations.html',
    'depends': [
        'base_address_extended',
        'account',
    ],
    'auto_install': ['account'],
    'data': [
        'data/res.city.csv'
    ],
    'demo': [
        'demo/demo_company.xml',
    ],
    'license': 'LGPL-3',
}
