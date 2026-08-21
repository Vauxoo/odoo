# Part of Odoo. See LICENSE file for full copyright and licensing details.
{
    "name": "LATAM Document",
    "version": "1.1",
    "author": "ADHOC SA",
    'category': 'Accounting/Localizations',
    "summary": "LATAM Document Types",
    "depends": [
        "account",
        "account_debit_note",
    ],
    "data": [
        'views/account_journal_view.xml',
        'views/account_move_line_view.xml',
        'views/account_move_view.xml',
        'views/l10n_latam_document_type_view.xml',
        'views/report_templates.xml',
        'report/invoice_report_view.xml',
        'wizards/account_move_reversal_view.xml',
        'security/ir.access.csv',
    ],
    'license': 'LGPL-3',
}
