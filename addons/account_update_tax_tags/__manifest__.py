{
    'name': 'Account - Allow updating tax grids',
    'category': 'Accounting/Accounting',
    'summary': 'Allow updating tax grids on existing entries',
    'depends': ['account'],
    'data': [
        'views/res_config_settings_views.xml',
        'wizard/account_update_tax_tags_wizard.xml',
        'security/ir.access.csv',
    ],
    'author': 'Odoo S.A.',
    'license': 'LGPL-3',
}
