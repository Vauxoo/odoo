{
    'name': "OdooBot - HR",
    'summary': """Bridge module between hr and mailbot.""",
    'website': "https://www.odoo.com/app/discuss",
    'category': 'Productivity/Discuss',
    'depends': ['mail_bot', 'hr'],
    'auto_install': True,
    'data': [
        'views/res_users_views.xml',
    ],
    'author': 'Odoo S.A.',
    'license': 'LGPL-3',
}
