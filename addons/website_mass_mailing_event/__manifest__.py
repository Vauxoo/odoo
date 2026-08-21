{
    'name': "Mass mailing on website events",
    'summary': 'Add pre-filled snippets in mass_mailing with an event snapshot',
    'category': 'Marketing/Email Marketing/Website',
    'depends': ['mass_mailing', 'website_event'],
    'assets': {
        'mass_mailing.assets_builder': [
            'website_mass_mailing_event/static/src/builder/**/*',
        ],
    },
    'data': [
        'views/snippets_themes.xml',
        'views/snippets/s_event_snapshot.xml',
    ],
    'auto_install': True,
    'author': 'Odoo S.A.',
    'license': 'LGPL-3',
}
