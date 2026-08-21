# Part of Odoo. See LICENSE file for full copyright and licensing details.

{
    'name': 'Drop Shipping',
    'category': 'Supply Chain/Inventory',
    'summary': 'Drop Shipping',
    'depends': ['sale_purchase_stock'],
    'data': [
        'data/stock_data.xml',
        'views/sale_order_views.xml',
        'views/stock_picking_views.xml',
        'views/purchase_order_views.xml'
    ],
    'demo': [
        'data/stock_dropshipping_demo.xml',
    ],
    'uninstall_hook': "uninstall_hook",
    'author': 'Odoo S.A.',
    'license': 'LGPL-3',
}
