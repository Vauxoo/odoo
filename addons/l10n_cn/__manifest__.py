# Part of Odoo. See LICENSE file for full copyright and licensing details.
{
    'name': 'China - Accounting',
    'icon': '/account/static/description/l10n.png',
    'countries': ['cn'],
    'version': '1.8',
    'category': 'Accounting/Localizations/Account Charts',
    'author': 'openerp-china',
    'maintainer': 'jeff@osbzr.com',
    'website': 'https://www.odoo.com/documentation/latest/applications/finance/fiscal_localizations.html',
    'depends': [
        'base',
        'account',
    ],
    'auto_install': ['account'],
    'data': [
        'data/account_tax_report_data.xml',
        'views/account_move_view.xml',
        'views/account_report.xml',
        'views/report_voucher.xml',
    ],
    'demo': [
        'demo/demo_company.xml',
        'demo/demo_company_asbe.xml',
    ],
    'license': 'LGPL-3',
}
