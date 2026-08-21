# Part of Odoo. See LICENSE file for full copyright and licensing details.
{
    'name': 'Mexico - Accounting',
    'website': 'https://www.odoo.com/documentation/latest/applications/finance/fiscal_localizations/mexico.html',
    'icon': '/account/static/description/l10n.png',
    'countries': ['mx'],
    'version': '2.3',
    'author': 'Vauxoo',
    'category': 'Accounting/Localizations/Account Charts',
    'depends': [
        'account',
    ],
    'auto_install': ['account'],
    'data': [
        'data/account.account.tag.csv',
        'data/account_report_diot.xml',
        'views/account_views.xml',
        'views/account_tax_view.xml',
        'views/res_config_settings_views.xml',
        "data/l10n_mx_uom.xml",
    ],
    'demo': [
        'demo/demo_company.xml',
    ],
    'license': 'LGPL-3',
    'post_init_hook': '_enable_group_uom_post_init',
}
