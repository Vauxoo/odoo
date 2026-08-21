# Part of Odoo. See LICENSE file for full copyright and licensing details.
{
    'name': 'Send SMS to Visitor',
    'category': 'Website/Website',
    'sequence': 54,
    'summary': 'Allows to send sms to website visitor',
    'depends': ['website', 'sms'],
    'data': [
        'views/website_visitor_views.xml',
    ],
    'auto_install': True,
    'author': 'Odoo S.A.',
    'license': 'LGPL-3',
}
