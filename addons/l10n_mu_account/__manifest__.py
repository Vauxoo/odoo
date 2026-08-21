# Part of Odoo. See LICENSE file for full copyright and licensing details.
{
    "name": "Mauritius - Accounting",
    'countries': ['mu'],
    "category": "Accounting/Localizations/Account Charts",
    "author": "Odoo S.A.",
    "depends": [
        "account",
    ],
    "auto_install": ["account"],
    "data": [
        "data/tax_report-mu.xml",
        "views/report_invoice.xml",
    ],
    "demo": [
        "demo/demo_company.xml",
    ],
    "license": "LGPL-3",
}
