# Part of Odoo. See LICENSE file for full copyright and licensing details.

{
    'name': 'Cloudflare Turnstile',
    'category': 'Website/Website',
    'depends': ['website'],
    'data': [
        'views/res_config_settings_view.xml',
    ],
    'assets': {
        'web.assets_frontend': [
            'website_cf_turnstile/static/src/interactions/**/*.js',
            'website_cf_turnstile/static/src/interactions/**/*.xml',
        ],
        'web.assets_unit_tests': [
            'website_cf_turnstile/static/tests/**/*',
        ],
        'web.assets_unit_tests_setup': [
            'website_cf_turnstile/static/src/interactions/**/*.js',
            'website_cf_turnstile/static/src/interactions/**/*.xml',
        ],
    },
    'author': 'Odoo S.A.',
    'license': 'LGPL-3',
}
