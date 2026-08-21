# Part of Odoo. See LICENSE file for full copyright and licensing details.

{
    'name': 'Phone Numbers Validation',
    'version': '2.1',
    'summary': 'Validate and format phone numbers',
    'sequence': 9999,
    'category': 'Hidden',
    'data': [
        'views/phone_blacklist_views.xml',
        'views/res_partner_views.xml',
        'wizard/phone_blacklist_remove_view.xml',
        'security/ir.access.csv',
    ],
    'depends': [
        'base',
        'mail',
    ],
    'auto_install': True,
    'author': 'Odoo S.A.',
    'license': 'LGPL-3',
}
