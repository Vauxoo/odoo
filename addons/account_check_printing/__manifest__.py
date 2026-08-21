# Part of Odoo. See LICENSE file for full copyright and licensing details.

{
    'name': 'Check Printing Base',
    'category': 'Accounting/Accounting',
    'summary': 'Check printing basic features',
    'depends': ['account'],
    'data': [
        'data/account_check_printing_data.xml',
        'views/account_journal_views.xml',
        'views/account_payment_views.xml',
        'views/res_config_settings_views.xml',
        'wizard/print_prenumbered_checks_views.xml',
        'security/ir.access.csv',
    ],
    'post_init_hook': 'create_check_sequence_on_bank_journals',
    'author': 'Odoo S.A.',
    'license': 'LGPL-3',
}
