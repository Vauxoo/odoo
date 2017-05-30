# coding: utf-8
# Copyright 2016 Vauxoo (https://www.vauxoo.com) <info@vauxoo.com>
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).

import logging
from odoo import SUPERUSER_ID, api

_logger = logging.getLogger(__name__)


def execute_update_fiscal_positions(cr):
    """This code are made in order to update the catalog for fiscal positions
    that are used as "fiscal regime" in CFDI generation. The catalog was
    updated, and need the news records"""
    with api.Environment.manage():
        env = api.Environment(cr, SUPERUSER_ID, {})
        _logger.info('Update catalog for Fiscal Position')
        # Inactivate old fiscal positions used as Regimen fiscal
        old_positions = [p for p in env['account.fiscal.position'].search(
            [('tax_ids', '=', False)]) if p.get_external_id()[p.id].startswith(
                'l10n_mx')]
        name_old_positions = []
        for position in old_positions:
            position.active = False
            name_old_positions.append(position.name)
        template = env.ref('l10n_mx.mx_coa')
        for company in env['res.company'].search([]):
            positions = env['account.fiscal.position.template'].search([
                ('chart_template_id', '=', template.id),
                ('name', 'not in', name_old_positions),
                ('tax_ids', '=', False)])
            for position in positions:
                template.create_record_with_xmlid(
                    company, position, 'account.fiscal.position', {
                        'company_id': company.id,
                        'name': position.name,
                        'note': position.note})


def migrate(cr, version):
    execute_update_fiscal_positions(cr)
