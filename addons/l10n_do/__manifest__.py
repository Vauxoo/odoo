# Part of Odoo. See LICENSE file for full copyright and licensing details.
{
    'name': 'Dominican Republic - Accounting',
    'icon': '/account/static/description/l10n.png',
    'countries': ['do'],
    'version': '2.0',
    'category': 'Accounting/Localizations/Account Charts',
    'author': 'Gustavo Valverde - iterativo | Consultores de Odoo (http://iterativo.do)',
    'website': 'https://www.odoo.com/documentation/latest/applications/finance/fiscal_localizations.html',
    'depends': [
        'account',
        'l10n_latam_base',
        'l10n_latam_invoice_document',
    ],
    'auto_install': ['account'],
    'data': [
        'data/account_account_tag_data.xml',
        'data/account_tax_report_data.xml',
        'data/l10n_latam_identification_type_data.xml',
        'data/l10n_latam_document_type_data.xml',
        'views/account_move_views.xml',
        'views/account_tax_views.xml',
    ],
    'demo': [
        'demo/demo_company.xml',
        'demo/demo_res_partner.xml',
        'demo/demo_account_journal.xml',
    ],
    'license': 'LGPL-3',
}
