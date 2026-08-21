# Part of Odoo. See LICENSE file for full copyright and licensing details.
{
    'name': 'Purchase Alternative',
    'version': '0.1',
    'category': 'Supply Chain/Purchase',
    'depends': ['purchase'],
    'demo': ['data/purchase_alternative_demo.xml'],
    'data': [
        'views/purchase_views.xml',
        'wizard/purchase_alternative_warning.xml',
        'wizard/purchase_alternative_create.xml',
        'security/ir.access.csv',
    ],
    'assets': {
        'web.assets_backend': [
            'purchase_alternative/static/src/*/**.js',
            'purchase_alternative/static/src/*/**.scss',
            'purchase_alternative/static/src/*/**.xml',
        ],
    },
    'author': 'Odoo S.A.',
    'license': 'LGPL-3',
}
