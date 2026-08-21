# Part of Odoo. See LICENSE file for full copyright and licensing details.

{
    'name': 'Resource',
    'version': '1.1',
    'category': 'Hidden',
    'depends': ['base', 'web'],
    'data': [
        'data/resource_data.xml',
        'data/ir_cron.xml',
        'views/resource_resource_views.xml',
        'views/resource_calendar_leaves_views.xml',
        'views/resource_calendar_attendance_views.xml',
        'views/resource_calendar_views.xml',
        'views/menuitems.xml',
        'security/ir.access.csv',
    ],
    'demo': [
        'data/resource_demo.xml',
    ],
    'assets': {
        'web.assets_backend': [
            'resource/static/src/**/*',
        ],
        'web.assets_unit_tests': [
            'resource/static/tests/**/*',
        ],
        'im_livechat.embed_assets_unit_tests_setup': [
            "resource/static/tests/mock_server/**/*",
        ],
    },
    'author': 'Odoo S.A.',
    'license': 'LGPL-3',
}
