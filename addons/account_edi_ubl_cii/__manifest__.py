{
    'name': "Import/Export electronic invoices with UBL/CII",
    'category': 'Accounting/Accounting',
    'depends': ['account'],
    'data': [
        'data/uom_data.xml',
        'data/cii_22_templates.xml',
        'data/ir_config_parameter_data.xml',
        'views/account_tax_views.xml',
        'views/account_move_views.xml',
        'views/res_partner_views.xml',
        'views/uom_uom_views.xml',
        'report/account_edi_ubl_cii_report_templates.xml',
    ],
    'assets': {
        'web.assets_backend': [
            'account_edi_ubl_cii/static/src/scss/**/*',
        ],
    },
    'auto_install': True,
    'author': 'Odoo S.A.',
    'license': 'LGPL-3',
    'uninstall_hook': 'uninstall_hook',
}
