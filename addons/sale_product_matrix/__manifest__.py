# Part of Odoo. See LICENSE file for full copyright and licensing details.

{
    "name": "Sale Matrix",
    "summary": "Add variants to Sales Order through a grid entry.",
    "category": "Sales/Sales",
    "depends": ["sale", "product_matrix"],
    "data": [
        "views/product_template_views.xml",
        "views/sale_order_views.xml",
        "report/sale_report_templates.xml",
    ],
    "demo": ["data/product_matrix_demo.xml"],
    "assets": {"web.assets_backend": ["sale_product_matrix/static/src/**/*"]},
    "author": "Odoo S.A.",
    "license": "LGPL-3",
}
