{
    'name': 'Translation Mode',
    'category': 'Hidden',
    'summary': 'In-context and interactive translation mode to streamline the module translation process using Weblate',
    'depends': ['web'],
    'data': [
        'data/config_parameter.xml',
        'views/translation_mode_settings.xml',
    ],
    'assets': {
        'web.assets_backend': [
            'test_translation_mode/static/src/**/*',
        ],
        'web.assets_frontend': [
            'test_translation_mode/static/src/**/*',
        ],
        'web.assets_unit_tests': [
            'test_translation_mode/static/tests/**/*',
        ],
    },
    'post_init_hook': 'post_init_hook',
    'uninstall_hook': 'uninstall_hook',
    'author': 'Odoo S.A.',
    'license': 'LGPL-3',
}
