# Part of Odoo. See LICENSE file for full copyright and licensing details.
{
    'name': 'Belgium - Accounting',
    'website': 'https://www.odoo.com/documentation/latest/applications/finance/fiscal_localizations/belgium.html',
    'version': '2.0',
    'icon': '/account/static/description/l10n.png',
    'countries': ['be'],
    'category': 'Accounting/Localizations/Account Charts',
    'author': 'Noviat, Odoo S.A.',
    'depends': [
        'account',
        'account_edi_ubl_cii',
    ],
    'auto_install': ['account'],
    'data': [
        'data/account_tax_report_data.xml',
        'data/l10n_be_sequence_data.xml',
        'data/menuitem_data.xml',
    ],
    'demo': [
        'demo/demo_company.xml',
    ],
    'license': 'LGPL-3',
}
