# Part of Odoo. See LICENSE file for full copyright and licensing details.
{
    'name': 'Switzerland - Accounting',
    'website': 'https://www.odoo.com/documentation/latest/applications/finance/fiscal_localizations/switzerland.html',
    'icon': '/account/static/description/l10n.png',
    'countries': ['ch'],
    'version': '11.3',
    'category': 'Accounting/Localizations/Account Charts',
    'depends': [
        'account',
        'account_edi_ubl_cii',
        'l10n_din5008',
    ],
    'auto_install': ['account'],
    'data': [
        'data/account_tax_report_data.xml',
        'report/swissqr_report.xml',
        'views/res_bank_view.xml',
        'views/account_invoice.xml',
        'views/setup_wizard_views.xml',
        'views/qr_invoice_wizard_view.xml',
        'views/account_payment_view.xml',
        'security/ir.access.csv',
    ],
    'demo': [
        'demo/account_cash_rounding.xml',
        'demo/demo_company.xml',
        'demo/res_partner_demo.xml',
    ],
    'post_init_hook': 'post_init',
    'assets': {
        'web.report_assets_common': [
            'l10n_ch/static/src/scss/**/*',
        ],
    }
,
    'author': 'Odoo S.A.',
    'license': 'LGPL-3',
}
