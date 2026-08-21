# Part of Odoo. See LICENSE file for full copyright and licensing details.
{
    'name': 'Czech - Accounting',
    'icon': '/account/static/description/l10n.png',
    'countries': ['cz'],
    'version': '1.1',
    'author': '26HOUSE (http://www.26house.com)',
    'website': 'https://www.odoo.com/documentation/latest/applications/finance/fiscal_localizations.html',
    'category': 'Accounting/Localizations/Account Charts',
    'depends': [
        'account',
        'account_edi_ubl_cii',
        'base_address_extended',
    ],
    'auto_install': ['account'],
    'data': [
        'views/res_partner_views.xml',
        'data/tax_report.xml',
        'data/l10n_cz.tax_office.csv',
        'data/res_country_data.xml',
        'views/report_invoice.xml',
        'views/res_company_views.xml',
        'views/report_template.xml',
        'views/tax_office_view.xml',
        'security/ir.access.csv',
    ],
    'demo': [
        'demo/demo_company.xml',
    ],
    'license': 'LGPL-3',
}
