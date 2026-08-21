{
    'name': "Indian - E-invoicing",
    'version': "1.03.00",
    'countries': ['in'],
    'category': "Accounting/Localizations/EDI",
    'depends': [
        "l10n_in",
    ],
    'data': [
        'views/account_move_views.xml',
        'views/edi_pdf_report.xml',
        'views/res_config_settings_views.xml',
        'views/account_journal_dashboard_views.xml',
        'wizard/l10n_in_edi_cancel_views.xml',
        'security/ir.access.csv',
    ],
    'demo': [
        "demo/demo_company.xml",
    ],
    'author': "Odoo S.A.",
    'license': "LGPL-3",
}
