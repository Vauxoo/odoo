# Part of Odoo. See LICENSE file for full copyright and licensing details.

{
    "name": "Zambia - Accounting",
    "countries": ["zm"],
    "version": "1.0.0",
    "category": "Accounting/Localizations/Account Charts",
    "author": "Odoo S.A.",
    "license": "LGPL-3",
    "depends": [
        "account",
    ],
    "auto_install": ["account"],
    "data": [
        "data/account_tax_report_data.xml",
        "views/report_invoice.xml",
    ],
    "demo": [
        "demo/demo_company.xml",
    ]
}
