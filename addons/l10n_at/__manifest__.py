# Part of Odoo. See LICENSE file for full copyright and licensing details.
{
    'name': 'Austria - Accounting',
    'icon': '/account/static/description/l10n.png',
    'countries': ['at'],
    'version': '3.2.1',
    'author': 'WT-IO-IT GmbH, Wolfgang Taferner (https://www.wt-io-it.at)',
    'website': 'https://www.odoo.com/documentation/latest/applications/finance/fiscal_localizations.html',
    'category': 'Accounting/Localizations/Account Charts',
    'summary': 'Austrian Standardized Charts & Tax',
    'depends': [
        'account',
        'account_edi_ubl_cii',
        'l10n_din5008',
    ],
    'auto_install': ['account'],
    'data': [
        'data/account_account_tag.xml',
        'data/account.account.tag.csv',
        'data/account_tax_report_data.xml',
    ],
    'demo': [
        'demo/demo_company.xml',
    ],
    'license': 'LGPL-3',
}
