# Part of Odoo. See LICENSE file for full copyright and licensing details.

{
    'name': 'Test - Base Automation',
    'category': 'Hidden',
    'sequence': 9877,
    'summary': 'Base Automation Tests: Ensure Flow Robustness',
    'depends': ['base_automation'],
    'data': [
        'security/ir.access.csv',
    ],
    'assets': {
        'web.assets_tests': [
            'test_base_automation/static/tests/**/*',
        ],
    },
    'author': 'Odoo S.A.',
    'license': 'LGPL-3',
}
