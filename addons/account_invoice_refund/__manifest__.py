{
    'name': 'Product Refund Accounts',
    'version': '12.0.1.0.0',
    'author': 'Vauxoo',
    'category': 'Localization',
    'license': 'LGPL-3',
    'summary': 'Adds refund accounts to products and product categories.',
    'depends': [
        'l10n_mx_edi',
        'account_accountant',
    ],
    'data': [
        'views/product.xml',
    ],
    'installable': True,
    'auto_install': False,
}
