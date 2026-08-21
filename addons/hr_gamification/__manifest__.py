# Part of Odoo. See LICENSE file for full copyright and licensing details.
{
    'name': 'HR Gamification',
    'category': 'Human Resources',
    'depends': ['gamification', 'hr'],
    'data': [
        'security/gamification_security.xml',
        'wizard/gamification_badge_user_wizard_views.xml',
        'views/gamification_views.xml',
        'views/hr_employee_views.xml',
        'security/ir.access.csv',
        ],
    'auto_install': True,
    'assets': {
        'web.assets_backend': [
            'hr_gamification/static/src/**/*',
        ],
        "web.assets_unit_tests": [
            "hr_gamification/static/tests/**/*",
        ],
    },
    'author': 'Odoo S.A.',
    'license': 'LGPL-3',
    'uninstall_hook': 'uninstall_hook',
}
