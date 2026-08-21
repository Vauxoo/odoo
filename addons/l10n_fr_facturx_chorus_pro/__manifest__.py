# Part of Odoo. See LICENSE file for full copyright and licensing details.

{
    'name': 'France - BIS3 integration for Chorus Pro',
    'countries': ['fr'],
    'category': 'Accounting/Localizations/EDI',
    'depends': [
        'account',
        'account_edi_ubl_cii',
        'l10n_fr_account',
    ],
    'data': [
        'views/account_move_views.xml',
        'views/report_invoice.xml',
    ],
    'author': 'Odoo S.A.',
    'license': 'LGPL-3',
}
