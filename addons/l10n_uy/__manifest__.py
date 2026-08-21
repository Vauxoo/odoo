# Part of Odoo. See LICENSE file for full copyright and licensing details.
{
    'name': 'Uruguay - Accounting',
    'website': 'https://www.odoo.com/documentation/latest/applications/finance/fiscal_localizations/uruguay.html',
    'icon': '/account/static/description/l10n.png',
    'countries': ['uy'],
    'version': '0.1',
    'author': 'Uruguay l10n Team, Guillem Barba, ADHOC',
    'category': 'Accounting/Localizations/Account Charts',
    'depends': [
        'account',
        'l10n_latam_invoice_document',
        'l10n_latam_base',
    ],
    'auto_install': ['account'],
    'data': [
        'data/account_tax_report_data.xml',
        'data/l10n_latam.document.type.csv',
        'data/l10n_latam_identification_type_data.xml',
        'data/res_partner_data.xml',
        'data/res_currency_data.xml',
        'views/account_tax_views.xml',
    ],
    'demo': [
        'demo/demo_company.xml',
        'demo/res_currency_rate_demo.xml',
        'demo/account_customer_refund_demo.xml',
        'demo/account_supplier_refund_demo.xml',
    ],
    'license': 'LGPL-3',
}
