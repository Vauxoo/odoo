{
    'name': 'test-uuid-ids',
    'version': '0.1',
    'category': 'Hidden/Tests',
    'description': """A module to test models whose records are identified by UUIDv7 ids.""",
    'depends': ['base'],
    'data': [
        'ir.model.access.csv',
    ],
    'pre_init_hook': 'pre_init_hook',
    'license': 'LGPL-3',
}
