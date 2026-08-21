# Part of Odoo. See LICENSE file for full copyright and licensing details.

{
    'name': 'EU One Stop Shop (OSS)',
    'category': 'Accounting/Localizations',
    'depends': ['account'],
    'data': [
        'data/account_account_tag.xml',
    ],
    'uninstall_hook': 'l10n_eu_oss_uninstall',
    'author': 'Odoo S.A.',
    'license': 'LGPL-3',
}
