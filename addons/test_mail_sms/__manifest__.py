
{
    'name': 'SMS Tests',
    'category': 'Hidden',
    'sequence': 9876,
    'summary': 'SMS Tests: performances and tests specific to SMS',
    'depends': [
        'mail',
        'sms',
        'sms_twilio',
        'test_orm',
    ],
    'data': [
        'security/ir.access.csv',
    ],
    'author': 'Odoo S.A.',
    'license': 'LGPL-3',
}
