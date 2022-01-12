# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from psycopg2.extensions import TransactionRollbackError
from odoo import api, fields, models, _
from odoo.tools.float_utils import float_compare


class StockBackorderConfirmation(models.TransientModel):
    _name = 'stock.backorder.confirmation'
    _description = 'Backorder Confirmation'

    pick_ids = fields.Many2many('stock.picking', 'stock_picking_backorder_rel')

    @api.one
    def _process(self, cancel_backorder=False):
        auto_commit = self.env['ir.config_parameter'].sudo().get_param('auto_commit_process_backorders')
        for pick_id in self.pick_ids:
            for attempt in range(3):
                try:
                    with self.env.cr.savepoint():
                        if cancel_backorder:
                            moves_to_log = {}
                            for move in pick_id.move_lines:
                                if float_compare(move.product_uom_qty, move.quantity_done,
                                                 precision_rounding=move.product_uom.rounding) > 0:
                                    moves_to_log[move] = (move.quantity_done, move.product_uom_qty)
                            if moves_to_log:
                                pick_id._log_less_quantities_than_expected(moves_to_log)
                        pick_id.action_done()
                        if cancel_backorder:
                            backorder_pick = self.env['stock.picking'].search([('backorder_id', '=', pick_id.id)])
                            backorder_pick.action_cancel()
                            pick_id.message_post(body=_("Back order <em>%s</em> <b>cancelled</b>.") % (
                                ",".join([b.name or '' for b in backorder_pick])))
                        break
                except TransactionRollbackError as tre:
                    if attempt < 2:
                        continue
                    raise tre
            if auto_commit:
                self.env.cr.commit()

    def process(self):
        self._process()

    def process_cancel_backorder(self):
        self._process(cancel_backorder=True)
