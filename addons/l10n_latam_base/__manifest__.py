# Part of Odoo. See LICENSE file for full copyright and licensing details.
{
    'name': 'LATAM Localization Base',
    'category': 'Accounting/Localizations',
    'sequence': 14,
    'author': 'Odoo S.A., ADHOC SA',
    'summary': 'LATAM Identification Types',
    'depends': [
        'contacts',
        'account',
    ],
    'data': [
        'data/res_country_group.xml',
        'data/l10n_latam.identification.type.csv',
        'views/res_partner_view.xml',
        'views/l10n_latam_identification_type_view.xml',
        'views/portal_address_templates.xml',
        'security/ir.access.csv',
    ],
    'assets': {
        'web.assets_frontend': [
            'l10n_latam_base/static/src/components/select_menu_wrapper/**.*',
        ],
    },
    'post_init_hook': '_set_default_identification_type',
    'license': 'LGPL-3',
}
