{
    'name': 'Link Tracker',
    'category': 'Website/Website',
    'summary': 'Generate trackable & short URLs',
    'depends': ['website', 'link_tracker'],
    'data': [
        'views/link_tracker_views.xml',
        'views/website_links_template.xml',
        'views/website_links_graphs.xml',
        'security/ir.access.csv',
    ],
    'auto_install': True,
    'assets': {
        'web.assets_frontend': [
            'website_links/static/src/components/*.js',
            'website_links/static/src/interactions/*.js',
            'website_links/static/src/css/website_links.css',
            'website_links/static/src/xml/*.xml',
        ],
        'web.assets_tests': [
            'website_links/static/tests/**/*',
        ],
        'website.assets_editor': [
            'website_links/static/src/services/website_custom_menus.js',
        ],
    },
    'author': 'Odoo S.A.',
    'license': 'LGPL-3',
}
