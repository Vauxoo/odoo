# Part of Odoo. See LICENSE file for full copyright and licensing details.
{
    'name': 'Base import module',
    'category': 'Hidden/Tools',
    'depends': ['web'],
    'auto_install': True,
    'data': [
        'views/base_import_module_view.xml',
        'views/ir_module_views.xml',
        'security/ir.access.csv',
    ],
    'assets': {
        'web.assets_backend': [
            'base_import_module/static/src/**/*',
        ],
        'web.assets_unit_tests': [
            'base_import_module/static/tests/**/*.test.js',
        ],
    },
    'author': 'Odoo S.A.',
    'license': 'LGPL-3',
}
