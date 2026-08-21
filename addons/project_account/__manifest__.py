# Part of Odoo. See LICENSE file for full copyright and licensing details.
{
    'name': "Project - Account",
    'summary': "project profitability items computation",
    'category': 'Accounting/Accounting',
    'depends': ['account', 'project'],
    'auto_install': True,
    'author': 'Odoo S.A.',
    'license': 'LGPL-3',
    'data': [
        'views/project_project_views.xml',
        'views/project_task_views.xml',
        'views/project_sharing_project_task_views.xml',
    ],
}
