# Part of Odoo. See LICENSE file for full copyright and licensing details.
{
    'name': "Sales - Service",
    'summary': "Interaction between Sales and services apps (project and planning)",
    'category': 'Sales/Sales',
    'depends': ['sale_management'],
    'assets': {
        'web.assets_backend': [
            'sale_service/static/src/**/*',
        ],
    },
    'author': 'Odoo S.A.',
    'license': 'LGPL-3',
}
