
{
    'name': 'Events Sales',
    'version': '1.3',
    'category': 'Marketing/Events',
    'website': 'https://www.odoo.com/app/events',
    'depends': ['event_product', 'sale_management'],
    'data': [
        'views/event_registration_views.xml',
        'views/event_views.xml',
        'views/product_template_views.xml',
        'views/sale_order_views.xml',
        'data/event_sale_data.xml',
        'data/mail_templates.xml',
        'report/event_sale_report_views.xml',
        'security/event_security.xml',
        'wizard/event_edit_registration.xml',
        'wizard/event_configurator_views.xml',
        'security/ir.access.csv',
    ],
    'demo': [
        'data/event_sale_demo.xml',
        'data/event_registration_demo.xml',  # needs event_sale_demo
    ],
    'auto_install': True,
    'assets': {
        'web.assets_backend': [
            'event_sale/static/src/**/*',
        ],
        'web.assets_tests': [
            'event_sale/static/tests/tours/**/*',
        ],
    },
    'author': 'Odoo S.A.',
    'license': 'LGPL-3',
}
