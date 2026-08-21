# Part of Odoo. See LICENSE file for full copyright and licensing details.

{
    'name': 'Dashboards',
    'category': 'Productivity',
    'sequence': 225,
    'summary': 'Build your own dashboards',
    'depends': ['spreadsheet_dashboard'],
    'data': [
        'views/board_views.xml',
        'security/ir.access.csv',
        ],
    'assets': {
        'web.assets_backend': [
            'board/static/src/**/*.scss',
            'board/static/src/**/*.js',
            'board/static/src/**/*.xml',
        ],
        'web.assets_unit_tests': [
            'board/static/tests/**/*.test.js',
        ],
    },
    'author': 'Odoo S.A.',
    'license': 'LGPL-3',
}
