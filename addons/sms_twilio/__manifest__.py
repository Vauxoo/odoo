{
    'name': 'Twilio SMS',
    'summary': 'Send SMS messages using Twilio',
    'category': 'Hidden/Tools',
    'depends': [
        'sms',
    ],
    'data': [
        'views/res_config_settings_views.xml',
        'views/sms_sms_views.xml',
        'wizard/sms_twilio_account_manage_views.xml',
        'security/ir.access.csv',
    ],
    'assets': {
        'web.assets_backend': [
            'sms_twilio/static/src/**/*',
        ],
    },
    'author': 'Odoo S.A.',
    'license': 'LGPL-3',
}
