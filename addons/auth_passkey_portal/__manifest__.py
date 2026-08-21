{
    'name': 'Passkeys Portal',
    'summary': 'Passkeys for portal users',
    'category': 'Hidden/Tools',
    'depends': ['auth_passkey', 'portal'],
    'data': [
        'views/templates.xml',
    ],
    'assets': {
        'web.assets_frontend': [
            'auth_passkey_portal/static/src/**',
        ],
        'web.assets_tests': [
            'auth_passkey_portal/static/tests/tours/*.js',
        ],
    },
    'author': 'Odoo S.A.',
    'license': 'LGPL-3',
    'auto_install': True,
}
