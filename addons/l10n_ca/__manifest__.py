# Part of Odoo. See LICENSE file for full copyright and licensing details.
{
    'name': 'Canada - Accounting',
    'version': '1.1',
    'icon': '/account/static/description/l10n.png',
    'countries': ['ca'],
    'author': 'Savoir-faire Linux (https://www.savoirfairelinux.com); Odoo S.A.',
    'website': 'https://www.odoo.com/documentation/latest/applications/finance/fiscal_localizations.html',
    'category': 'Accounting/Localizations/Account Charts',
    'depends': [
        'account',
    ],
    'auto_install': ['account'],
    'data': [
        'data/tax_report.xml',
        'views/res_partner_view.xml',
        'views/res_company_view.xml',
        'views/report_invoice.xml',
        'views/report_template.xml',
    ],
    'demo': [
        'demo/demo_company.xml',
    ],
    'license': 'LGPL-3',
}
