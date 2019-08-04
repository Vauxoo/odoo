from odoo import models


class AccountMoveLine(models.Model):
    _inherit = 'account.move.line'

    def get_invoice_line_account(self, type, product, fpos, company):
        if type not in ('out_refund', 'in_refund'):
            return super(AccountMoveLine, self).get_invoice_line_account(
                type, product, fpos, company)
        accounts = product.product_tmpl_id.get_product_accounts(fpos)
        account_map = {
            'out_refund': 'income_refund',
            'in_refund': 'expense_refund',
        }
        return accounts[account_map[type]]
