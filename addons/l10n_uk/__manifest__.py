# Part of Odoo. See LICENSE file for full copyright and licensing details.
{
    'name': 'United Kingdom - Accounting',
    'icon': '/account/static/description/l10n.png',
    'countries': ['gb'],
    'version': '1.1',
    'category': 'Accounting/Localizations/Account Charts',
    'author': 'SmartMode LTD',
    'website': 'https://www.odoo.com/documentation/latest/applications/finance/fiscal_localizations/united_kingdom.html',
    'depends': [
        'account',
    ],
    'auto_install': ['account'],
    'data': [
        'data/country_group.xml',
        'data/l10n_uk_chart_data.xml',
        'data/account_tax_report_data.xml',
    ],
    'demo': [
        'demo/l10n_uk_demo.xml',
        'demo/demo_company.xml',
    ],
    'license': 'LGPL-3',
}
