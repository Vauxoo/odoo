from odoo import models, api


class AccountInvoiceLine(models.Model):
    _inherit = 'account.invoice.line'

    @api.v8
    def get_invoice_line_account(self, type, product, fpos, company):
        if type not in ('out_refund', 'in_refund'):
            return super(AccountInvoiceLine, self).get_invoice_line_account(
                type, product, fpos, company)
        accounts = product.product_tmpl_id.get_product_accounts(fpos)
        account_map = {
            'out_refund': 'income_refund',
            'in_refund': 'expense_refund',
        }
        return accounts[account_map[type]]


class AccountInvoice(models.Model):
    _inherit = 'account.invoice'

    @api.multi
    @api.returns('self')
    def refund(self, date_invoice=None, date=None, description=None,
               journal_id=None):
        """Use refund accounts when the credit note is created from the invoice
        """
        res = super(AccountInvoice, self).refund(
            date_invoice, date, description, journal_id)
        lines = res.mapped('invoice_line_ids').filtered(lambda x: (
            x.invoice_type == 'out_refund' and (
                x.product_id.property_account_income_refund_id or
                x.product_id.categ_id.property_account_income_refund_id)) or (
            x.invoice_type == 'in_refund' and (
                x.product_id.property_account_expense_refund_id or
                x.product_id.categ_id.property_account_expense_refund_id)))
        for line in lines:
            line.account_id = line.get_invoice_line_account(
                line.invoice_type, line.product_id,
                line.invoice_id.fiscal_position_id, line.company_id)
        return res
