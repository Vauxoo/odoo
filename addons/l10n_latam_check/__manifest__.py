# Part of Odoo. See LICENSE file for full copyright and licensing details.
{
    'name': 'Third Party and Deferred/Electronic Checks Management',
    'category': 'Accounting/Localizations',
    'summary': 'Checks Management',
    'author': 'ADHOC SA',
    'license': 'LGPL-3',
    'depends': [
        'account',
    ],
    'data': [
        'data/account_payment_method_data.xml',
        'wizards/l10n_latam_payment_mass_transfer_views.xml',
        'views/account_payment_view.xml',
        'views/l10n_latam_check_view.xml',
        'views/report_payment_receipt_templates.xml',
        'wizards/account_payment_register_views.xml',
        'security/ir.access.csv',
    ],
}
