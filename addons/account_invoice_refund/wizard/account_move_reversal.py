from odoo import models


class AccountMoveReversal(models.TransientModel):

    _inherit = 'account.move.reversal'

    def reverse_moves(self):
        res = super(AccountMoveReversal, self).reverse_moves()
        move_ids = self.env['account.move'].search(
            [('id', '=', res.get('res_id'))])
        lines = move_ids.mapped('invoice_line_ids').filtered(lambda x: (
            x.move_id.type == 'out_refund' and (
                x.product_id.property_account_income_refund_id or
                x.product_id.categ_id.property_account_income_refund_id)) or (
            x.move_id.type == 'in_refund' and (
                x.product_id.property_account_expense_refund_id or
                x.product_id.categ_id.property_account_expense_refund_id)))
        for line in lines:
            line.account_id = line.get_invoice_line_account(
                line.move_id.type, line.product_id,
                line.move_id.fiscal_position_id, line.company_id)
        return res
