# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.
# Copyright (c) 2017 Vauxoo (http://vauxoo.com).
from odoo import api, models, _

import logging
_logger = logging.getLogger(__name__)


class AccountChartTemplate(models.Model):
    _inherit = "account.chart.template"
    _description = "Templates for Account Chart"

    @api.multi
    def _prepare_all_journals(self, acc_template_ref, company,
                              journals_dict=None):
        if company.country_id != self.env.ref('base.pe'):
            return super(AccountChartTemplate, self)._prepare_all_journals(
                acc_template_ref, company, journals_dict)

        def _get_default_account(journal_vals, type='debit'):
            default_account = False
            if journal['type'] == 'sale':
                default_account = acc_template_ref.get(
                    self.property_account_income_categ_id.id)
            elif journal['type'] == 'purchase':
                default_account = acc_template_ref.get(
                    self.property_account_expense_categ_id.id)
            elif (journal['type'] == 'general' and
                  journal['code'] == _('EXCH')):
                if type == 'credit':
                    default_account = acc_template_ref.get(
                        self.income_currency_exchange_account_id.id)
                else:
                    default_account = acc_template_ref.get(
                        self.expense_currency_exchange_account_id.id)
            return default_account

        sequence_fac = self.env['account.journal']._create_sequence({
            'prefix': 'F001-',
            'name': _('Factura de Venta')
        })
        refund_sequence_fac = self.env['account.journal']._create_sequence({
            'prefix': 'CF01-',
            'name': _(u'Nota de Crédito Factura'),
        })

        sequence_bol = self.env['account.journal']._create_sequence({
            'prefix': 'B001-',
            'name': _('Boleta de Venta')
        })
        refund_sequence_bol = self.env['account.journal']._create_sequence({
            'prefix': 'CB01-',
            'name': _(u'Nota de Crédito Boleta de Venta'),
        })

        sequence_gr = self.env['account.journal']._create_sequence({
            'prefix': 'G001-',
            'name': _(u'Guía de Remisión'),
        })

        journals = [{
            'name': _('Factura de Venta'),
            'type': 'sale',
            'code': 'FAC',
            'favorite': True,
            'sequence': 1,
            'sequence_id': sequence_fac.id,
            'refund_sequence': True,
            'refund_sequence_id': refund_sequence_fac.id,
        }, {
            'name': _('Boleta de Venta'),
            'type': 'sale',
            'code': 'BOL',
            'favorite': True,
            'sequence': 2,
            'sequence_id': sequence_bol.id,
            'refund_sequence': True,
            'refund_sequence_id': refund_sequence_bol.id,
        }, {
            'name': _('Guía de Remisión'),
            'type': 'sale',
            'code': 'GR',
            'favorite': False,
            'sequence': 3,
            'sequence_id': sequence_gr.id,
        }, {
            'name': _('Vendor Bills'),
            'type': 'purchase',
            'code': _('BILL'),
            'favorite': True,
            'sequence': 4
        }, {
            'name': _('Miscellaneous Operations'),
            'type': 'general',
            'code': _('MISC'),
            'favorite': False,
            'sequence': 5
        }, {
            'name': _('Exchange Difference'),
            'type': 'general',
            'code': _('EXCH'),
            'favorite': False,
            'sequence': 6
        }]

        if journals_dict:
            journals.extend(journals_dict)

        self.ensure_one()
        journal_data = []
        for journal in journals:
            vals = {
                'type': journal['type'],
                'name': journal['name'],
                'code': journal['code'],
                'company_id': company.id,
                'default_credit_account_id': _get_default_account(journal,
                                                                  'credit'),
                'default_debit_account_id': _get_default_account(journal,
                                                                 'debit'),
                'show_on_dashboard': journal['favorite'],
                'sequence': journal['sequence'],
                'sequence_id': journal.get('sequence_id', False),
            }
            journal_data.append(vals)
        return journal_data
