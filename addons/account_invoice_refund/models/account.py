from odoo import models


class AccountMoveLine(models.Model):
    _inherit = 'account.move.line'

    def _get_computed_account(self):
        if self.move_id.type not in ('out_refund', 'in_refund'):
            return super(AccountMoveLine, self)._get_computed_account()
        accounts = self.product_id.product_tmpl_id.get_product_accounts()
        account_map = {
            'out_refund': 'income_refund',
            'in_refund': 'expense_refund',
        }
        return accounts[account_map[self.move_id.type]]
