{
    'name': '2FA Invite mail',
    'depends': ['auth_totp', 'mail'],
    'category': 'Extra Tools',
    'auto_install': True,
    'data': [
        'data/ir_action_data.xml',
        'data/mail_template_data.xml',
        'data/security_notifications_template.xml',
        'views/res_config_settings_views.xml',
        'views/res_users_views.xml',
        'views/templates.xml',
    ],
    'assets': {
        'web.assets_tests': [
            'auth_totp_mail/static/tests/**/*',
        ],
        'web.assets_backend': [
            'auth_totp_mail/static/src/services/check_identity/*',
        ],
        'web.assets_frontend': [
            'auth_totp_mail/static/src/services/check_identity/*',
        ],
    },
    'author': 'Odoo S.A.',
    'license': 'LGPL-3',
}
