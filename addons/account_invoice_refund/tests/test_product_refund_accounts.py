from odoo.tests.common import TransactionCase


class TestProductRefundAccounts(TransactionCase):
    """Test cases for l10n_mx_edi_product_refund_account module"""

    def setUp(self):
        super(TestProductRefundAccounts, self).setUp()
        self.invoice = self.env['account.invoice'].create({
            'partner_id': self.env.ref('base.res_partner_12').id,
            'journal_id': self.env['account.journal'].search([
                ('code', '=', 'INV'),
            ], limit=1).id,
        })
        accounts = self.env['account.account']
        self.income_account = accounts.create({
            'code': '101.01.999',
            'name': 'Account Test Income',
            'deprecated': False,
            'user_type_id': self.env.ref(
                'account.data_account_type_other_income').id,
        })
        self.expense_account = accounts.create({
            'code': '101.02.999',
            'name': 'Account Test Expense',
            'deprecated': False,
            'user_type_id': self.env.ref(
                'account.data_account_type_expenses').id,
        })
        self.product_w_account = self.env['product.product'].create({
            'name': 'Product with account',
            'type': 'consu',
            'property_account_income_refund_id': self.expense_account.id,
            'property_account_expense_refund_id': self.income_account.id,
        })
        self.product_w_category = self.env['product.product'].create({
            'name': 'Product with category',
            'type': 'consu',
            'categ_id': self.env['product.category'].create({
                'name': 'Category with account',
                'property_account_income_refund_id': self.expense_account.id,
                'property_account_expense_refund_id': self.income_account.id,
            }).id,
        })
        self.product_default = self.env['product.product'].create({
            'name': 'Product with category',
            'type': 'consu',
            'categ_id': self.env['product.category'].create({
                'name': 'Category without account',
                'property_account_income_categ_id': self.income_account.id,
                'property_account_expense_categ_id': self.expense_account.id,
            }).id
        })

    def test_001_out_refund(self):
        self.invoice.write({
            'type': 'out_refund',
        })
        line = self.env['account.invoice.line'].new({
            'invoice_id': self.invoice.id,
            'product_id': self.product_w_account.id,
        })
        line._onchange_product_id()
        self.assertEquals(line.account_id, self.expense_account)
        line = self.env['account.invoice.line'].new({
            'invoice_id': self.invoice.id,
            'product_id': self.product_w_category.id,
        })
        line._onchange_product_id()
        self.assertEquals(line.account_id, self.expense_account)
        line = self.env['account.invoice.line'].new({
            'invoice_id': self.invoice.id,
            'product_id': self.product_default.id,
        })
        line._onchange_product_id()
        self.assertEquals(line.account_id, self.income_account)

    def test_002_in_refund(self):
        self.invoice.write({
            'type': 'in_refund',
        })
        line = self.env['account.invoice.line'].new({
            'invoice_id': self.invoice.id,
            'product_id': self.product_w_account.id,
        })
        line._onchange_product_id()
        self.assertEquals(line.account_id, self.income_account)
        line = self.env['account.invoice.line'].new({
            'invoice_id': self.invoice.id,
            'product_id': self.product_w_category.id,
        })
        line._onchange_product_id()
        self.assertEquals(line.account_id, self.income_account)
        line = self.env['account.invoice.line'].new({
            'invoice_id': self.invoice.id,
            'product_id': self.product_default.id,
        })
        line._onchange_product_id()
        self.assertEquals(line.account_id, self.expense_account)
