# Part of Odoo. See LICENSE file for full copyright and licensing details.

{
    'name': "Define Taxes as Python Code",
    'summary': "Use python code to define taxes",
    'category': 'Accounting/Accounting',
    'depends': ['account'],
    'data': [
        'views/account_tax_views.xml',
    ],
    'assets': {
        'web.assets_backend': [
            'account_tax_python/static/src/helpers/*.js',
        ],
        'web.assets_frontend': [
            'account_tax_python/static/src/helpers/*.js',
        ],
    },
    'author': 'Odoo S.A.',
    'license': 'LGPL-3',
}
