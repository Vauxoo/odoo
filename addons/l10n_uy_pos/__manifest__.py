# Part of Odoo. See LICENSE file for full copyright and licensing details.
{
    "name": "Uruguayan - Point of Sale",
    "category": "Accounting/Localizations/Point of Sale",
    "depends": [
        "l10n_uy",
        "point_of_sale",
    ],
    "assets": {
        "point_of_sale._assets_pos": ["l10n_uy_pos/static/src/**/*"],
    },
    "auto_install": True,
    'author': 'Odoo S.A.',
    "license": "LGPL-3",
}
