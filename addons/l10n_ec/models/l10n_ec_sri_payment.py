# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import fields, models


class L10n_EcSriPayment(models.Model):
    _name = 'l10n_ec.sri.payment'

    _description = "SRI Payment Method"
    _order = "sequence, id"

    sequence = fields.Integer(default=10)
    name = fields.Char(translate=True)
    code = fields.Char()
    active = fields.Boolean(default=True)
