# Part of Odoo. See LICENSE file for full copyright and licensing details.

{
    'name': 'Morocco - Accounting',
    'icon': '/account/static/description/l10n.png',
    'countries': ['ma'],
    'author': 'Odoo S.A.',
    'category': 'Accounting/Localizations/Account Charts',
    'depends': [
        'base',
        'account',
    ],
    'auto_install': ['account'],
    'data': [
        'data/account_tax_report_data.xml',
        'views/portal_address_templates.xml',
    ],
    'assets': {
        'web.assets_frontend': [
            'l10n_ma/static/src/interactions/**/*',
        ],
    },
    'demo': [
        'demo/demo_company.xml',
    ],
    'license': 'LGPL-3',
}
