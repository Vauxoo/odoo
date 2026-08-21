{
    'name' : 'Import/Export Invoices From XML/PDF',
    'category': 'Accounting/Accounting',
    'depends' : ['account'],
    'data': [
        'views/account_edi_document_views.xml',
        'views/account_move_views.xml',
        'views/account_journal_views.xml',
        'data/cron.xml',
        'security/ir.access.csv',
    ],
    'author': 'Odoo S.A.',
    'license': 'LGPL-3',
}
