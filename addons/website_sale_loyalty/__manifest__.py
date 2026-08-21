# Part of Odoo. See LICENSE file for full copyright and licensing details.

{
    "name": "Coupons, Promotions, Gift Card and Loyalty for eCommerce",
    "summary": """Use coupon, promotion, gift cards and loyalty programs in your eCommerce store""",
    "category": "Website/Website",
    "depends": ["website_sale", "website_links", "sale_loyalty"],
    "data": [
        "views/loyalty_card_views.xml",
        "views/loyalty_program_views.xml",
        "views/website_sale_templates.xml",
        "views/website_sale_loyalty_menus.xml",
        "wizard/coupon_share_views.xml",
        "wizard/res_config_settings_views.xml",
        "security/ir.access.csv",
    ],
    "demo": ["data/product_demo.xml"],
    "auto_install": ["website_sale", "sale_loyalty"],
    "assets": {
        "web.assets_frontend": [
            "website_sale_loyalty/static/src/js/**/*",
            "website_sale_loyalty/static/src/interactions/**/*",
        ],
        "web.assets_tests": ["website_sale_loyalty/static/tests/**/*"],
    },
    "author": "Odoo S.A.",
    "license": "LGPL-3",
}
