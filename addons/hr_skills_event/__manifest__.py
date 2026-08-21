# Part of Odoo. See LICENSE file for full copyright and licensing details.

{
    'name': 'Skills Events',
    'category': 'Hidden',
    'summary': 'Link training events to resume of your employees',
    'depends': ['hr_skills', 'event'],
    'data': [
        'views/hr_resume_line_views.xml',
        'views/event_event_views.xml',
        'views/hr_views.xml',
    ],
    'auto_install': True,
    'author': 'Odoo S.A.',
    'license': 'LGPL-3',
}
