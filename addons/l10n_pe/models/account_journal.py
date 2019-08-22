from odoo import models, api


class AccountJournal(models.Model):
    _inherit = "account.journal"

    @api.model
    def _get_sequence_prefix(self, code, refund=False):
        """For peruvian companies we can not use sequences with **/** due to the edi generation which need in the
        sequence a plain text ended by a *-* and the length of this prefix"""
        if self.env.company.country_id != self.env.ref('base.pe'):
            return super()._get_sequence_prefix(code, refund=refund)
        prefix = code.upper()
        if refund:
            prefix = 'R' + prefix[:-1]
        return prefix + '-'

    @api.model
    def _create_sequence(self, vals, refund=False):
        """For Peruvian companies, a number reset by date do not make sense due to the fact that we can not use a free
        prefix the format does not have enough space to put a year on it or any other char, then with this approach we
        are avoiding the default behavior there."""
        res = super()._create_sequence(vals, refund=refund)
        if self.env.company.country_id != self.env.ref('base.pe'):
            return res
        res.write({'use_date_range': False})
        return res
