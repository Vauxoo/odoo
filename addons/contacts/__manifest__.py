# Part of Odoo. See LICENSE file for full copyright and licensing details.


{
    'name': 'Contacts',
    'category': 'Sales/CRM',
    'sequence': 150,
    'summary': 'Centralize your address book',
    'depends': ['base', 'mail', 'web_hierarchy'],
    'data': [
        'views/contact_views.xml',
    ],
    'demo': [
        'data/mail_demo.xml',
    ],
    'application': True,
    'author': 'Odoo S.A.',
    'license': 'LGPL-3',
    'assets': {
        'web.assets_backend': [
            'contacts/static/src/views/contacts_hierarchy/contacts_hierarchy_card.scss',
        ],
        'web.assets_tests': [
            'contacts/static/tests/tours/**/*',
        ],
    }
}
