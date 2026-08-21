# Part of Odoo. See LICENSE file for full copyright and licensing details.
{
    'name': 'Luxembourg - Accounting',
    'website': 'https://www.odoo.com/documentation/latest/applications/finance/fiscal_localizations/luxembourg.html',
    'icon': '/account/static/description/l10n.png',
    'countries': ['lu'],
    'version': '2.2',
    'category': 'Accounting/Localizations/Account Charts',
    'author': 'Odoo S.A., ADN, ACSONE SA/NV',
    'depends': [
        'account',
        'account_edi_ubl_cii',
    ],
    'auto_install': ['account'],
    'data': [
        'data/account.account.tag.csv',
        'data/l10n_lu_chart_data.xml',
        'data/tax_report/section_1.xml',
        'data/tax_report/section_2.xml',
        'data/tax_report/sections_34.xml',
        'data/tax_report/tax_report.xml',
    ],
    'demo': [
        'demo/demo_company.xml',
    ],
    'post_init_hook': '_post_init_hook',
    'license': 'LGPL-3',
}
