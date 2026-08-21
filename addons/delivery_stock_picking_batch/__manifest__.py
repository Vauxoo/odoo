# Part of Odoo. See LICENSE file for full copyright and licensing details.

{
    'name': 'Delivery Stock Picking Batch',
    'category': 'Supply Chain/Inventory',
    'summary': 'Batch Transfer, Carrier',
    'depends': ['stock_delivery', 'stock_picking_batch'],
    'data': [
        'views/stock_picking_type_views.xml',
    ],
    'auto_install': True,
    'author': 'Odoo S.A.',
    'license': 'LGPL-3',
}
