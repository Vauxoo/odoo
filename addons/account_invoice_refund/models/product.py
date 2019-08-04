from odoo import models, api, fields


class ProductCategory(models.Model):
    _inherit = 'product.category'

    property_account_income_refund_id = fields.Many2one(
        'account.account', "Income Refund Account",
        company_dependent=True, domain=[('deprecated', '=', False)],
        help="Used as default value on the customer credit notes lines. "
             "Leave empty to use the income account.")
    property_account_expense_refund_id = fields.Many2one(
        'account.account', "Expense Refund Account",
        company_dependent=True, domain=[('deprecated', '=', False)],
        help="Used as default value on the vendor refunds lines. "
             "Leave empty to use the expense account.")


class ProductTemplate(models.Model):
    _inherit = 'product.template'

    property_account_income_refund_id = fields.Many2one(
        'account.account', "Income Refund Account",
        company_dependent=True, domain=[('deprecated', '=', False)],
        help="Used as default value on the customer credit notes lines. "
             "Leave empty to use the account from the product category.")
    property_account_expense_refund_id = fields.Many2one(
        'account.account', "Expense Refund Account",
        company_dependent=True, domain=[('deprecated', '=', False)],
        help="Used as default value on the vendor refunds lines. "
             "Leave empty to use the account from the product category.")

    @api.multi
    def _get_product_accounts(self):
        accounts = super(ProductTemplate, self)._get_product_accounts()
        accounts.update({
            'income_refund': self.property_account_income_refund_id or (
                self.categ_id.property_account_income_refund_id or
                accounts.get('income')),
            'expense_refund': self.property_account_expense_refund_id or (
                self.categ_id.property_account_expense_refund_id or
                accounts.get('expense')),
        })
        return accounts
