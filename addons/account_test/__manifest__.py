# Part of Odoo. See LICENSE file for full copyright and licensing details.

# Copyright (c) 2011 CCI Connect asbl (http://www.cciconnect.be) All Rights Reserved.
#                       Philmer <philmer@cciconnect.be>

{
    'name': 'Accounting Consistency Tests',
    'category': 'Accounting/Accounting',
    'depends': ['account'],
    'data': [
        'views/accounting_assert_test_views.xml',
        'report/accounting_assert_test_reports.xml',
        'data/accounting_assert_test_data.xml',
        'report/report_account_test_templates.xml',
        'security/ir.access.csv',
    ],
    'author': 'Odoo S.A.',
    'license': 'LGPL-3',
}
