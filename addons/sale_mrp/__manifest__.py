# Part of Odoo. See LICENSE file for full copyright and licensing details.


{
    'name': 'Sales and MRP Management',
    'category': 'Sales/Sales',
    'depends': ['mrp', 'sale_stock'],
    'data': [
        'views/mrp_production_views.xml',
        'views/sale_order_views.xml',
        'views/sale_portal_templates.xml',
        'security/ir.access.csv',
    ],
    'auto_install': True,
    'author': 'Odoo S.A.',
    'license': 'LGPL-3',
}
