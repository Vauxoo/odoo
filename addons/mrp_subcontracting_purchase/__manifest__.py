# Part of Odoo. See LICENSE file for full copyright and licensing details.

{
    'name': 'Purchase and Subcontracting Management',
    'version': '0.1',
    'category': 'Supply Chain/Purchase',
    'depends': ['mrp_subcontracting_account', 'purchase_mrp'],
    'data': [
        'views/purchase_order_views.xml',
        'views/stock_picking_views.xml',
    ],
    'demo': [
        'data/mrp_subcontracting_purchase_demo.xml',
    ],
    'auto_install': True,
    'author': 'Odoo S.A.',
    'license': 'LGPL-3',
}
