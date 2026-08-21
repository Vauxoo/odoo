# Part of Odoo. See LICENSE file for full copyright and licensing details.

# Thanks to Landoo and the Spanish community
# Specially among others Aritz Olea, Luis Salvatierra, Josean Soroa

{
    'name': "Spain - TicketBAI",
    'version': '1.1',
    'category': 'Accounting/Localizations/EDI',
    'depends': [
        'l10n_es',
        'certificate',
    ],
    'data': [
        'data/template_invoice.xml',
        'data/template_LROE_bizkaia.xml',
        'data/ir_config_parameter.xml',

        'views/account_move_view.xml',
        'views/l10n_es_edi_tbai_certificate_views.xml',
        'views/report_invoice.xml',
        'views/res_config_settings_views.xml',
        'views/res_company_views.xml',

        'wizards/account_move_reversal_views.xml',
        'security/ir.access.csv',
    ],
    'demo': [
        'demo/demo_certificate.xml',
        'demo/demo_res_partner.xml',
        'demo/demo_company.xml',
    ],
    'author': 'Odoo S.A.',
    'license': 'LGPL-3',
}
