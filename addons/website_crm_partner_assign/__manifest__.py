# Part of Odoo. See LICENSE file for full copyright and licensing details.

{
    'name': 'Resellers',
    'category': 'Website/Website',
    'summary': 'Publish your resellers/partners and forward leads to them',
    'version': '1.3',
    'depends': ['base_geolocalize', 'crm', 'account', 'website_partnership',
                'website_partner', 'website_google_map', 'portal'],
    'data': [
        'data/crm_lead_merge_template.xml',
        'data/crm_tag_data.xml',
        'data/mail_template_data.xml',
        'data/res_partner_activation_data.xml',
        'data/portal_entry_data.xml',
        'wizard/crm_forward_to_partner_view.xml',
        'views/res_partner_views.xml',
        "views/website_page_views.xml",
        'views/res_partner_activation_views.xml',
        'views/res_partner_grade_views.xml',
        'views/crm_lead_views.xml',
        'views/website_crm_partner_assign_templates.xml',
        'views/partner_assign_menus.xml',
        'report/crm_partner_report_view.xml',
        'security/ir.access.csv',
    ],
    'demo': [
        'data/res_partner_demo.xml',
        'data/crm_lead_demo.xml',
    ],
    'assets': {
        'web.assets_frontend': [
            'website_crm_partner_assign/static/src/interactions/**/*',
        ],
        'website.website_builder_assets': [
            'website_crm_partner_assign/static/src/website_builder/**/*',
        ],
        'html_builder.assets_inside_builder_iframe': [
            'website_crm_partner_assign/static/src/scss/crm_partner_assign.scss',
        ],
    },
    'author': 'Odoo S.A.',
    'license': 'LGPL-3',
}
