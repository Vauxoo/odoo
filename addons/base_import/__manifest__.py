{
    'name': 'Base import',
    'depends': ['web'],
    'version': '2.0',
    'category': 'Hidden/Tools',
    'auto_install': True,
    'data': [
        'security/ir.access.csv',
    ],
    'assets': {
        'web.assets_backend': [
            'base_import/static/src/**/*.scss',
            'base_import/static/src/**/*.js',
            'base_import/static/src/**/*.xml',
        ],
        'web.assets_unit_tests': [
            'base_import/static/tests/**/*.test.js',
        ],
    },
    'author': 'Odoo S.A.',
    'license': 'LGPL-3',
}
