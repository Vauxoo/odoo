{
    'name': 'Discuss Tracking',
    'category': 'Productivity/Discuss',
    'depends': ['mail'],
    'summary': 'Technical tracking of discussion and message-related data',
    'author': 'Odoo S.A.',
    'license': 'LGPL-3',
    'data': [
        'views/mail_message_views.xml',
        'views/mail_tracking_value_views.xml',
        'views/mail_menus.xml',
        'security/ir.access.csv',
    ],
}
