# Part of Odoo. See LICENSE file for full copyright and licensing details.

{
    'name': 'MTO Sale <-> Purchase',
    'category': 'Sales/Sales',
    'summary': 'SO/PO relation in case of MTO',
    'depends': ['sale_stock', 'purchase_stock', 'sale_purchase'],
    'data': [
        'views/purchase_order_views.xml',
        'views/stock_picking_views.xml',
    ],
    'auto_install': True,
    'author': 'Odoo S.A.',
    'license': 'LGPL-3',
}
