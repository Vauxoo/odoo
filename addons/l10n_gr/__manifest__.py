# Part of Odoo. See LICENSE file for full copyright and licensing details.

{
    'name': 'Greece - Accounting',
    'icon': '/account/static/description/l10n.png',
    'countries': ['gr'],
    'author': 'P. Christeas, Odoo S.A.',
    'category': 'Accounting/Localizations/Account Charts',
    'depends': [
        'account',
        'account_edi_ubl_cii',
    ],
    'auto_install': ['account'],
    'data': [
        'data/account_tax_report_data.xml',
    ],
    'demo': [
        'demo/demo_company.xml',
    ],
    'license': 'LGPL-3',
}
