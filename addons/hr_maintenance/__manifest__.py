
{
    'name': 'Maintenance - HR',
    'sequence': 125,
    'category': 'Human Resources',
    'depends': ['hr', 'maintenance'],
    'summary': 'Equipment, Assets, Internal Hardware, Allocation Tracking',
    'data': [
        'security/equipment.xml',
        'views/maintenance_views.xml',
        'views/hr_views.xml',
    ],
    'auto_install': True,
    'author': 'Odoo S.A.',
    'license': 'LGPL-3',
}
