# Part of Odoo. See LICENSE file for full copyright and licensing details.

{
    'name': 'Timesheet when on Time Off',
    'category': 'Human Resources',
    'summary': 'Schedule timesheet when on time off',
    'depends': ['hr_timesheet', 'hr_holidays'],
    'data': [
        'views/res_config_settings_views.xml',
        'views/project_task_views.xml',
        'security/ir.access.csv',

    ],
    'demo': [
        'data/holiday_timesheets_demo.xml',
    ],
    'auto_install': True,
    'post_init_hook': 'post_init',
    'author': 'Odoo S.A.',
    'license': 'LGPL-3',
}
