# Part of Odoo. See LICENSE file for full copyright and licensing details.

{
    'name': 'Landed Costs With Subcontracting order',
    'summary': 'Advanced views to manage landed cost for subcontracting orders',
    'depends': ['mrp_landed_costs', 'mrp_subcontracting'],
    'category': 'Supply Chain/Manufacturing',
    'data': [
        'views/stock_landed_cost_views.xml',
    ],
    'auto_install': True,
    'author': 'Odoo S.A.',
    'license': 'LGPL-3',
}
