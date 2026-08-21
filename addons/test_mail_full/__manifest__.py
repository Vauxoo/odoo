
{
    'name': 'Mail Tests (Full)',
    'category': 'Hidden',
    'sequence': 9876,
    'summary': 'Mail Tests: performances and tests specific to mail with all sub-modules',
    'depends': [
        'mail',
        'mail_bot',
        'portal',
        'rating',
        # 'snailmail',
        'mass_mailing',
        'mass_mailing_sms',  # adds portal
        'phone_validation',
        'sms',
        'test_mail',
        'test_mail_sms',
        'test_mass_mailing',
    ],
    'data': [
        'data/mail_message_subtype_data.xml',
        'views/test_portal_template.xml',
        'security/ir.access.csv',
    ],
    'assets': {
        'web.assets_unit_tests': [
            'test_mail_full/static/tests/**/*',
            ('remove', 'test_mail_full/static/tests/tours/**/*'),
        ],
        'web.assets_tests': [
            'test_mail_full/static/tests/tours/**/*',
        ],
    },
    'author': 'Odoo S.A.',
    'license': 'LGPL-3',
}
