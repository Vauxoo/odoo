# Part of Odoo. See LICENSE file for full copyright and licensing details.
{
    'name': 'Purchase Agreements',
    'version': '0.1',
    'category': 'Supply Chain/Purchase',
    'depends': ['purchase'],
    'demo': ['data/purchase_requisition_demo.xml'],
    'data': [
        'data/purchase_requisition_data.xml',
        'views/product_views.xml',
        'views/purchase_views.xml',
        'views/purchase_requisition_views.xml',
        'report/purchase_requisition_report.xml',
        'report/report_purchaserequisition.xml',
        'security/ir.access.csv',
    ],
    'author': 'Odoo S.A.',
    'license': 'LGPL-3',
}
