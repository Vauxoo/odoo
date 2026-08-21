# Part of Odoo. See LICENSE file for full copyright and licensing details.

{
    'name': 'Landed Costs On MO',
    'summary': 'Landed Costs on Manufacturing Order',
    'depends': ['stock_landed_costs', 'mrp'],
    'category': 'Supply Chain/Manufacturing',
    'data': [
        'views/stock_landed_cost_views.xml',
    ],
    'auto_install': True,
    'author': 'Odoo S.A.',
    'license': 'LGPL-3',
}
