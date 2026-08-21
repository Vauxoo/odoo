{
    'name': 'Proxy features for account_edi',
    'category': 'Accounting/Accounting',
    'depends': ['account', 'certificate'],
    'data': [
        'views/account_edi_proxy_user_views.xml',
        'security/ir.access.csv',
    ],
    'author': 'Odoo S.A.',
    'license': 'LGPL-3',
    'post_init_hook': '_create_demo_config_param',
}
