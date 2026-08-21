# Part of Odoo. See LICENSE file for full copyright and licensing details.
{
    'name': "Purchase Matrix",
    'summary': "Add variants to your purchase orders through an Order Grid Entry.",
    'category': 'Supply Chain/Purchase',
    'depends': ['purchase', 'product_matrix'],
    'data': [
        'views/purchase_views.xml',
        'report/purchase_quotation_templates.xml',
        'report/purchase_order_templates.xml',
    ],
    'assets': {
        'web.assets_backend': [
            'purchase_product_matrix/static/src/**/*',
        ],
        'web.assets_tests': [
            'purchase_product_matrix/static/tests/tours/**/*',
        ],
    },
    'author': 'Odoo S.A.',
    'license': 'LGPL-3',
}
