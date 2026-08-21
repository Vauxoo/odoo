# Part of Odoo. See LICENSE file for full copyright and licensing details.

{
    'name': 'Newsletter Subscribe SMS Template',
    'summary': 'Attract visitors to subscribe to mailing lists',
    'category': 'Website/Website',
    'depends': ['website_mass_mailing', 'mass_mailing_sms'],
    'data': [
        'views/snippets/snippets_templates.xml',
        'data/ir_model_data.xml',
    ],
    'auto_install': True,
    'author': 'Odoo S.A.',
    'license': 'LGPL-3',
    'assets': {
        'website.website_builder_assets': [
            'website_mass_mailing_sms/static/src/website_builder/**/*',
        ],
    },
}
