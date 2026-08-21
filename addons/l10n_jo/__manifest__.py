# Part of Odoo. See LICENSE file for full copyright and licensing details.
{
    'name': 'Jordan - Accounting',
    'countries': ['jo'],
    'category': 'Accounting/Localizations/Account Charts',
    'depends': [
        'account',
    ],
    'auto_install': ['account'],
    'data': [
        'data/account_tax_report_data.xml',
    ],
    'demo': [
        'demo/demo_company.xml',
        'demo/demo_partner.xml',
    ],
    'author': 'Odoo S.A.',
    'license': 'LGPL-3',
}
