# Part of Odoo. See LICENSE file for full copyright and licensing details.

{
    'name': 'Automation Rules',
    'category': 'Sales/Sales',
    'depends': ['base', 'digest', 'resource', 'mail', 'sms'],
    'data': [
        'data/base_automation_data.xml',
        'data/digest_data.xml',
        'views/base_automation_views.xml',
        'views/ir_actions_server_views.xml',
        'security/ir.access.csv',
    ],
    'assets': {
        'web.assets_backend': [
            'base_automation/static/src/**/*',
        ],
        'web.assets_unit_tests': [
            'base_automation/static/tests/**/*',
        ],
    },
    'author': 'Odoo S.A.',
    'license': 'LGPL-3',
}
