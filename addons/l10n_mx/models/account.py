# coding: utf-8
# Copyright 2016 Vauxoo (https://www.vauxoo.com) <info@vauxoo.com>
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).

import re
from odoo import models, api, fields, _


class AccountAccount(models.Model):
    _inherit = 'account.account'

    @api.multi
    def assign_account_tag(self):
        """Based on account code will be assigned by default the corresponding
        tag by tag code"""
        account_tag_obj = self.env['account.account.tag']
        for record in self:
            if not record.is_valid_account_number():
                continue
            account = record.get_account_tuple()
            tag_parent = account_tag_obj.search([
                ('name', 'ilike', str(account[0])),
                ('color', '=', 1)])
            tag = account_tag_obj.search([
                ('name', 'ilike', '%s.%s' % (account[0], account[1])),
                ('color', '=', 4)])
            tags = [tag_parent.id] if tag_parent else []
            tags.extend([tag.id] if tag else [])
            record.write({
                'tag_ids': [(4, tags)]})

    def search_regex(self):
        """ Review if the given number is a valid account number
        :return: the regex search None or regex object
        """
        return re.search(
            '^(?P<first>[1-8][0-9][0-9])[,.]'
            '(?P<second>[0-9][0-9])[,.]'
            '(?P<third>[0-9]{2,3})$', self.code)

    def is_valid_account_number(self):
        """:return: Boolean """
        return True if self.search_regex() else False

    def get_account_tuple(self):
        """:return: separate parts of the account"""
        return self.search_regex().groups()


class AccountAccountTag(models.Model):
    _inherit = 'account.account.tag'

    nature = fields.Selection([
        ('D', _('Debitable Account')), ('A', _('Creditable Account'))],
        help='Used in report of electronic accounting like account nature.')
