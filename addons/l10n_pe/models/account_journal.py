# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.
# Copyright (c) 2017 Vauxoo (http://vauxoo.com).
from odoo import api, models


class AccountJournal(models.Model):
    _inherit = "account.journal"

    @api.model
    def _create_sequence(self, vals, refund=False):
        if self.env.user.company_id.country_id != self.env.ref('base.pe'):
            return super(AccountJournal, self)._create_sequence(vals, refund)
        if not vals.get('prefix', False):
            vals['prefix'] = self._get_sequence_prefix(vals['code'], refund)
        seq = {
            'name': vals['name'],
            'implementation': 'no_gap',
            'prefix': vals.pop('prefix'),
            'padding': 8,
            'number_increment': 1,
            'use_date_range': True,
        }
        if 'company_id' in vals:
            seq['company_id'] = vals['company_id']
        return self.env['ir.sequence'].create(seq)
