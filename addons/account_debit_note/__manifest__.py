# Part of Odoo. See LICENSE file for full copyright and licensing details.

{
    'name': 'Debit Notes',
    'category': 'Accounting/Accounting',
    'summary': 'Debit Notes',
    'depends': ['account'],
    'data': [
        'wizard/account_debit_note_view.xml',
        'views/account_move_view.xml',
        'views/account_journal_views.xml',
        'views/report_invoice.xml',
        'security/ir.access.csv',
    ],
    'author': 'Odoo S.A.',
    'license': 'LGPL-3',
}
