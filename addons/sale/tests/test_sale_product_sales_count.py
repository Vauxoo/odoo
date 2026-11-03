# Part of Odoo. See LICENSE file for full copyright and licensing details.

from datetime import timedelta

from odoo import fields
from odoo.fields import Command
from odoo.tests import tagged

from odoo.addons.sale.tests.common import SaleCommon


@tagged('post_install', '-at_install')
class TestSaleProductSalesCount(SaleCommon):

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.uom_dozen = cls.quick_ref('uom.product_uom_dozen')
        cls.uom_dozen.active = True

    def _sold(self, lines, **order_values):
        order = self.env['sale.order'].create({
            'partner_id': self.partner.id,
            'order_line': [Command.create(line) for line in lines],
            **order_values,
        })
        return order

    def test_sales_count_counts_confirmed_lines_of_the_last_year(self):
        product = self.product
        self._sold([{'product_id': product.id, 'product_uom_qty': 3}]).action_confirm()
        # a dozen of a unit-based product counts 12
        self._sold([{
            'product_id': product.id, 'product_uom_qty': 2, 'product_uom_id': self.uom_dozen.id,
        }]).action_confirm()
        # not confirmed
        self._sold([{'product_id': product.id, 'product_uom_qty': 100}])
        # older than a year
        old_order = self._sold([{'product_id': product.id, 'product_uom_qty': 1000}])
        old_order.action_confirm()
        old_order.date_order = fields.Datetime.now() - timedelta(days=366)
        # sections and notes are not counted
        self._sold([
            {'display_type': 'line_section', 'name': 'Section'},
            {'product_id': product.id, 'product_uom_qty': 5, 'display_type': False},
            {'display_type': 'line_note', 'name': 'Note'},
        ]).action_confirm()

        product.invalidate_recordset(['sales_count'])
        self.assertEqual(product.sales_count, 3 + 24 + 5)
        self.assertEqual(product.product_tmpl_id.sales_count, product.sales_count)

    def test_sales_count_matches_the_sales_report(self):
        products = self.product + self.service_product
        for product in products:
            self._sold([
                {'product_id': product.id, 'product_uom_qty': 4},
                {'product_id': product.id, 'product_uom_qty': 1, 'product_uom_id': self.uom_dozen.id},
            ]).action_confirm()
        products.invalidate_recordset(['sales_count'])
        report = {
            product.id: qty
            for product, qty in self.env['sale.report']._read_group(
                [('product_id', 'in', products.ids), ('state', 'in', self.env['sale.report']._get_done_states())],
                ['product_id'],
                ['product_uom_qty:sum'],
            )
        }
        for product in products:
            self.assertEqual(product.sales_count, product.uom_id.round(report[product.id]))

    def test_sales_count_of_a_new_product_is_zero(self):
        new_product = self.env['product.product'].new({'name': 'New'})
        self.assertEqual(new_product.sales_count, 0)
