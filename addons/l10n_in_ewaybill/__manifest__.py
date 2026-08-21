# Part of Odoo. See LICENSE file for full copyright and licensing details.

{
    'name': """Indian - E-waybill""",
    'countries': ['in'],
    'version': '2.0',
    'category': 'Accounting/Localizations',
    'depends': [
        'l10n_in',
    ],
    'data': [
        'data/ewaybill_type_data.xml',
        'views/l10n_in_ewaybill_views.xml',
        'views/account_move_views.xml',
        'views/edi_pdf_report.xml',
        'views/res_config_settings_views.xml',
        'wizard/l10n_in_ewaybill_cancel_views.xml',
        'report/ewaybill_report_views.xml',
        'report/ewaybill_report.xml',
        'security/ir.access.csv',
    ],
    'iap_paid_service': True,
    # not auto_install because the company can be related to the service industry
    'author': 'Odoo S.A.',
    'license': 'LGPL-3',
}
