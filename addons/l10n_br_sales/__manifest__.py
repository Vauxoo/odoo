# Part of Odoo. See LICENSE file for full copyright and licensing details.
{
    'name': 'Brazil - Sale',
    'category': 'Sales/Sales',
    'depends': [
        'l10n_br',
        'sale',
    ],
    'data': [
        'views/sale_portal_templates.xml',
        'report/sale_order_templates.xml',
        'report/report_invoice_templates.xml',
    ],
    'auto_install': True,
    'author': 'Odoo S.A.',
    'license': 'LGPL-3',
}
