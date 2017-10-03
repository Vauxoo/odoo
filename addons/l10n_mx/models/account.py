# coding: utf-8
# Copyright 2016 Vauxoo (https://www.vauxoo.com) <info@vauxoo.com>
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).

from odoo import models, api, fields, _


class AccountJournal(models.Model):
    _inherit = 'account.journal'

    @api.model
    def _prepare_liquidity_account(self, name, company, currency_id, type):
        '''
        When preparing the values to use when creating the default debit and credit accounts of a
        liquidity journal, set the correct group for the mexican localization.
        '''
        res = super(AccountJournal, self)._prepare_liquidity_account(name, company, currency_id, type)
        if company.country_id.id == self.env.ref('base.mx').id:
            code_prefix = res.get('code')
            while code_prefix:
                maching_group = self.env['account.group'].search(
                    'code_prefix', '=', code_prefix)
                if maching_group:
                    res.update({'group_id': maching_group.id})
                    break
                code_prefix = code_prefix[:-1]
        return res


class AccountGroup(models.Model):
    _inherit = 'account.group'

    nature = fields.Selection([
        ('D', _('Debitable Account')), ('A', _('Creditable Account'))],
        help='Used in Mexican report of electronic accounting (account nature).')
