
{
    'name': 'Mail Tests',
    'category': 'Hidden',
    'sequence': 9876,
    'summary': 'Mail Tests: performances and tests specific to mail',
    'depends': [
        'mail',
        'test_orm',
        'mail_tracking',
    ],
    'data': [
        'data/data.xml',
        'data/mail_template_data.xml',
        'data/subtype_data.xml',
        'security/ir.access.csv',
    ],
    'assets': {
        'web.assets_unit_tests': [
            'test_mail/static/tests/**/*',
        ],
        'web.assets_tests': [
            'test_mail/static/tests/tours/*',
        ],
    },
    'author': 'Odoo S.A.',
    'license': 'LGPL-3',
}
