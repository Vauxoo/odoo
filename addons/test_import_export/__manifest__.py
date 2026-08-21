{
    'name': 'Test - Import & Export',
    'category': 'Hidden',
    'sequence': 3843,
    'summary': 'Base Import & Export Tests: Ensure Flow Robustness',
    # website is there only for MockRequest
    'depends': ['web', 'base_import', 'website', 'test_tools'],
    'data': [
        'security/ir.access.csv',
    ],
    'author': 'Odoo S.A.',
    'license': 'LGPL-3',
}
