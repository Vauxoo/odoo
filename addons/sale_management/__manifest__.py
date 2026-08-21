# Part of Odoo. See LICENSE file for full copyright and licensing details.

{
    "name": "Sales",
    "category": "Sales/Sales",
    "sequence": 5,
    "summary": "From quotations to invoices",
    "website": "https://www.odoo.com/app/sales",
    "depends": ["sale", "digest"],
    "data": [
        "data/digest_data.xml",
        # Define SO template views & actions before their place of use
        "views/sale_order_template_views.xml",
        "views/digest_views.xml",
        "views/res_config_settings_views.xml",
        "views/sale_order_views.xml",
        "views/sale_portal_templates.xml",
        "views/sale_management_menus.xml",
        'security/ir.access.csv',
    ],
    "demo": ["data/sale_order_template_demo.xml"],
    "assets": {
        "web.assets_backend": [
            "sale_management/static/src/fields/**/*",
            "sale_management/static/src/views/**/*",
        ],
        "web.assets_frontend": ["sale_management/static/src/interactions/**/*"],
        "web.assets_tests": ["sale_management/static/tests/tours/**/*"],
        "web.assets_unit_tests": [
            "sale_management/static/tests/mock_server/**/*",
            "sale_management/static/tests/sale_management_test_helpers.js",
            "sale_management/static/tests/**/*.test.js",
        ],
    },
    "application": True,
    "post_init_hook": "post_init_hook",
    "uninstall_hook": "uninstall_hook",
    "author": "Odoo S.A.",
    "license": "LGPL-3",
}
