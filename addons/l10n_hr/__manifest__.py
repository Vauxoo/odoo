# Part of Odoo. See LICENSE file for full copyright and licensing details.
{
    'name': 'Croatia - Accounting (Euro)',
    'website': 'https://www.odoo.com/documentation/latest/applications/finance/fiscal_localizations.html',
    'icon': '/account/static/description/l10n.png',
    'countries': ['hr'],
    'version': '13.0',
    'category': 'Accounting/Localizations/Account Charts',
    'depends': [
        'account',
    ],
    'auto_install': ['account'],
    'data': [
        'data/l10n_hr_chart_data.xml',
        'data/account_tax_report_data.xml',
    ],
    'demo': [
        'demo/demo_company.xml',
    ],
    'author': 'Odoo S.A.',
    'license': 'LGPL-3',
}
