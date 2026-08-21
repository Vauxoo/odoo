# Part of Odoo. See LICENSE file for full copyright and licensing details.
{
    'name': 'France - Accounting',
    'website': 'https://www.odoo.com/documentation/latest/applications/finance/fiscal_localizations/france.html',
    'icon': '/account/static/description/l10n.png',
    'version': '2.2',
    'countries': ['fr'],
    'category': 'Accounting/Localizations/Account Charts',
    'depends': [
        'account',
        'account_edi_ubl_cii',
        'l10n_fr',
    ],
    'auto_install': ['account'],
    'data': [
        'data/account_chart_template_data.xml',
        'data/account_data.xml',
        'data/tax_report_data.xml',
        'views/report_invoice.xml',
        'wizard/account_fr_fec_export_wizard_view.xml',
        'security/ir.access.csv',
    ],
    'demo': [
        'data/l10n_fr_account_demo.xml',
    ],
    'post_init_hook': '_l10n_fr_post_init_hook',
    'author': 'Odoo S.A.',
    'license': 'LGPL-3',
}
