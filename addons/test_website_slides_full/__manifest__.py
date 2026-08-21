# Part of Odoo. See LICENSE file for full copyright and licensing details.
{
    'name': 'Test Full eLearning Flow',
    'category': 'Hidden/Tests',
    'depends': [
        'website_sale_slides',
        'website_slides_forum',
        'website_slides_survey',
    ],
    'data': [
        'data/res_groups_data.xml',
    ],
    'demo': [
        'data/product_demo.xml',
    ],
    'assets': {
        'web.assets_tests': [
            'test_website_slides_full/static/tests/tours/**/*',
        ],
    },
    'author': 'Odoo S.A.',
    'license': 'LGPL-3',
}
