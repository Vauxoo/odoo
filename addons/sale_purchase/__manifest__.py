# Part of Odoo. See LICENSE file for full copyright and licensing details.

{
    'name': 'Sale Purchase',
    'summary': 'Sale based on service outsourcing.',
    'category': 'Sales/Sales',
    'depends': [
        'sale',
        'purchase',
    ],
    'data': [
        'data/mail_templates.xml',
        'views/product_views.xml',
        'views/sale_order_views.xml',
        'views/purchase_order_views.xml',
    ],
    'auto_install': True,
    'author': 'Odoo S.A.',
    'license': 'LGPL-3',
}
