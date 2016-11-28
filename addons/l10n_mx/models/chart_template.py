# coding: utf-8
# Copyright 2016 Vauxoo (https://www.vauxoo.com) <info@vauxoo.com>
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).

from odoo import models, api, _


class AccountChartTemplate(models.Model):
    _inherit = "account.chart.template"

    @api.multi
    def _load_template(
            self, company, code_digits=None, transfer_account_id=None,
            account_ref=None, taxes_ref=None):
        self.ensure_one()
        accounts, taxes = super(AccountChartTemplate, self)._load_template(
            company, code_digits=code_digits,
            transfer_account_id=transfer_account_id, account_ref=account_ref,
            taxes_ref=taxes_ref)
        account_tax_obj = self.env['account.tax']
        account_obj = self.env['account.account']
        # Due to the fact that the template does not have the fields
        # 'use_cash_basis' and 'cash_basis_account' we are making this ugly
        # hack which should be removed in master once those fields are add in
        # account.tax.template
        taxes_acc = {
            'ITAX_010-IN': account_obj.search([('code', '=', '208.01.01')]),
            'ITAX_160-IN': account_obj.search([('code', '=', '208.01.01')]),
            'ITAXR_04-OUT': account_obj.search([('code', '=', '216.13.01')]),
            'ITAXR_10-OUT': account_obj.search([('code', '=', '216.13.01')]),
            'ITAX_1067-OUT': account_obj.search([('code', '=', '216.13.01')]),
            'ITAX_167-OUT': account_obj.search([('code', '=', '216.13.01')]),
            'ITAX_010-OUT': account_obj.search([('code', '=', '208.01.01')]),
            'ITAX_160-OUT': account_obj.search([('code', '=', '208.01.01')])}

        for tax in self.tax_template_ids:
            if tax.description not in taxes_acc:
                continue
            account_tax_obj.browse(taxes.get(tax.id)).write({
                'use_cash_basis': True,
                'cash_basis_account': taxes_acc.get(tax.description).id,
            })
        return accounts, taxes

    @api.multi
    def generate_account(
            self, tax_template_ref, acc_template_ref, code_digits, company):
        res = super(AccountChartTemplate, self).generate_account(
            tax_template_ref, acc_template_ref, code_digits, company)
        self.env['account.account'].browse(res.values()).assign_account_tag()
        return res

    @api.model
    def generate_journals(self, acc_template_ref, company, journals_dict=None):
        res = super(AccountChartTemplate, self).generate_journals(
            acc_template_ref, company, journals_dict=journals_dict)
        journal_basis = self.env['account.journal'].search([
            ('type', '=', 'general'),
            ('code', '=', 'CBMX')], limit=1)
        company.write({'tax_cash_basis_journal_id': journal_basis.id})
        return res

    @api.multi
    def _prepare_all_journals(
            self, acc_template_ref, company, journals_dict=None):
        res = super(AccountChartTemplate, self)._prepare_all_journals(
            acc_template_ref, company, journals_dict=journals_dict)
        res.append({
            'type': 'general',
            'name': _('Effectively Paid'),
            'code': 'CBMX',
            'company_id': company.id,
            'default_credit_account_id': acc_template_ref.get(
                self.income_currency_exchange_account_id.id),
            'default_debit_account_id': acc_template_ref.get(
                self.expense_currency_exchange_account_id.id),
            'show_on_dashboard': True,
        })
        return res


class WizardMultiChartsAccounts(models.TransientModel):
    _inherit = 'wizard.multi.charts.accounts'

    @api.multi
    def execute(self):
        """Overwrite the account code to Undistributed Profits/Losses and
        write the tags in this account & in cash and bank"""
        res = super(WizardMultiChartsAccounts, self).execute()
        account_obj = self.env['account.account']
        # Overwrite this account code because this is created by python code
        # https://goo.gl/tiqfVm, and to get the chart template like the
        # Mexican charts needs.
        account = account_obj.search([
            ('code', '=', '999999'), ('user_type_id', '=', self.env.ref(
                "account.data_unaffected_earnings").id)])
        account.write({'code': '811.01.01'})
        account.assign_account_tag()
        type_liquidity = self.env.ref("account.data_account_type_liquidity").id
        account_obj.search([
            ('code', 'in', ('102.01.02', '101.01.01')),
            ('user_type_id', '=', type_liquidity)]).assign_account_tag()
        return res
