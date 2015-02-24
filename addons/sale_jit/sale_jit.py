# -*- coding: utf-8 -*-
##############################################################################
#
#    OpenERP, Open Source Management Solution
#    Copyright (C) 2004-2013 Tiny SPRL (<http://tiny.be>).
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU Affero General Public License as
#    published by the Free Software Foundation, either version 3 of the
#    License, or (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU Affero General Public License for more details.
#
#    You should have received a copy of the GNU Affero General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
##############################################################################

from openerp.osv import osv

class sale_order(osv.osv):
    _inherit = "sale.order"

    def action_ship_create(self, cr, uid, ids, context=None):
        context = context or {}
        context['no_run_at_create'] = True

        res = super(sale_order, self).action_ship_create(cr, uid, ids, context=context)

        procurement_obj = self.pool.get('procurement.order')
        order = self.browse(cr, uid, ids, context=context)[0]

        proc_ids = procurement_obj.search(cr, uid, [('origin', 'ilike', order.name)], context=context)
        while (proc_ids):
            procurement_obj.run(cr, uid, proc_ids, context=context)
            procurement_obj.check(cr, uid, proc_ids, context=context)
            proc_ids = procurement_obj.search(cr, uid, [('origin', 'ilike', order.name), ('state', '=', 'confirmed')], context=context)
        return res
