# Part of Odoo. See LICENSE file for full copyright and licensing details.
{
    'name': 'Slovak - Accounting',
    'icon': '/account/static/description/l10n.png',
    'countries': ['sk'],
    'author': '26HOUSE (http://www.26house.com)',
    'website': 'https://www.odoo.com/documentation/latest/applications/finance/fiscal_localizations.html',
    'category': 'Accounting/Localizations/Account Charts',
    'depends': [
        'account',
    ],
    'auto_install': ['account'],
    'data': [
        'data/tax_report.xml',
        'views/res_company_views.xml',
        'views/report_invoice.xml',
        'views/report_template.xml',
    ],
    'demo': [
        'demo/demo_company.xml',
    ],
    'license': 'LGPL-3',
}
