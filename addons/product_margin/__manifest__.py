# Part of Odoo. See LICENSE file for full copyright and licensing details.


{
    'name': 'Margins by Products',
    'category': 'Sales/Sales',
    'depends': ['account'],
    'data': [
        'wizard/product_margin_view.xml',
        'views/product_product_views.xml',
        'security/ir.access.csv',
    ],
    'author': 'Odoo S.A.',
    'license': 'LGPL-3',
}
