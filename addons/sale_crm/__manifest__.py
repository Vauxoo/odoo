# Part of Odoo. See LICENSE file for full copyright and licensing details.

{
    'name': 'Opportunity to Quotation',
    'category': 'Sales/Sales',
    'depends': ['sale', 'crm'],
    'data': [
        'data/crm_lead_merge_template.xml',
        'views/sale_order_views.xml',
        'views/crm_lead_views.xml',
        'views/crm_team_views.xml',
        'wizard/crm_opportunity_to_quotation_views.xml',
        'security/ir.access.csv',
    ],
    'auto_install': True,
    'uninstall_hook': 'uninstall_hook',
    'author': 'Odoo S.A.',
    'license': 'LGPL-3',
}
