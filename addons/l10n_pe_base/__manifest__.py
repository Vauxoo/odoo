# Part of Odoo. See LICENSE file for full copyright and licensing details.
{
    'name': 'Base Localization for Odoo Peru not account',
    'version': '2.0',
    'author': 'Vauxoo',
    'category': 'Localization',
    "description": """
Base data for Peru environments.
============================================

This module add the data needed for the res_partner model to have the right
format for the address in Peru. We are adding the data for the regional
information regional information and related to each level, meaning, states are
related to countries, city to state, district to city and we are adding the
complemented res_partner_view to show the accurate information of the address.

Another improvement this module has, is a fix to the base_vat and to check if
the document as VAT is what we need, returning the information needed for
identification purposes only.
""",
    'depends': [
        'base_vat',
        'base_address_extended',
        'base_address_city',
    ],
    "data": [
        'security/ir.model.access.csv',
        'data/res_country_data.xml',
        'data/res.city.csv',
        'data/res.district.csv',
        'views/res_partner_view.xml',
    ],
    'installable': True,
}
