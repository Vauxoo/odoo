{
    'name': 'Two-Factor Authentication (TOTP)',
    'depends': ['web'],
    'category': 'Extra Tools',
    'auto_install': True,
    'data': [
        'data/ir_action_data.xml',
        'views/res_users_views.xml',
        'views/templates.xml',
        'wizard/auth_totp_wizard_views.xml',
        'security/ir.access.csv',
    ],
    'assets': {
        'web.assets_tests': [
            'auth_totp/static/tests/**/*',
        ],
        'web.assets_backend': [
            'auth_totp/static/src/scss/**/*',
            'auth_totp/static/src/services/check_identity/*',
        ],
        'web.assets_frontend': [
            'auth_totp/static/src/services/check_identity/*',
        ],
    },
    'author': 'Odoo S.A.',
    'license': 'LGPL-3',
}
