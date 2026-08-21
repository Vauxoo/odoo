# Part of Odoo. See LICENSE file for full copyright and licensing details.
{
    'name' : 'Fleet',
    'version' : '0.1',
    'sequence': 185,
    'category': 'Human Resources/Fleet',
    'website' : 'https://www.odoo.com/app/fleet',
    'summary' : 'Manage your fleet and track car costs',
    'depends': [
        'base',
        'mail',
    ],
    'data': [
        'security/fleet_security.xml',
        'views/fleet_vehicle_model_views.xml',
        'views/fleet_vehicle_views.xml',
        'views/fleet_vehicle_cost_views.xml',
        'views/fleet_board_view.xml',
        'views/mail_activity_views.xml',
        'views/res_config_settings_views.xml',
        'views/fleet_vehicle_odometer_report.xml',
        'views/res_partner_views.xml',
        'data/fleet_cars_data.xml',
        'data/fleet_data.xml',
        'data/mail_message_subtype_data.xml',
        'data/mail_activity_type_data.xml',
        'wizard/fleet_vehicle_send_mail_views.xml',
        'security/ir.access.csv',
    ],

    'demo': ['data/fleet_demo.xml'],

    'application': True,
    'assets': {
        'web.assets_backend': [
            'fleet/static/src/**/*',
        ],
    },
    'author': 'Odoo S.A.',
    'license': 'LGPL-3',
}
