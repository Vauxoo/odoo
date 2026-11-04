from datetime import date, datetime

from odoo.tests import common
from odoo.tools.partitioning import PartitionSpec


class TestPartitionSpec(common.TransactionCase):

    def test_spec_rejects_unknown_keys(self):
        with self.assertRaisesRegex(ValueError, "must be a dict with keys among"):
            PartitionSpec.from_model(self.env['test_new_api.partition.event'], {'key': 'date', 'step': 1})

    def test_spec_rejects_strategy_other_than_range(self):
        with self.assertRaisesRegex(ValueError, "only range partitioning is supported"):
            PartitionSpec.from_model(self.env['test_new_api.partition.event'], {'by': 'list', 'key': 'date'})

    def test_spec_rejects_key_not_stored(self):
        with self.assertRaisesRegex(ValueError, "must be a stored field"):
            PartitionSpec.from_model(self.env['test_new_api.partition.event'], {'key': 'display_name'})

    def test_spec_rejects_key_not_required(self):
        with self.assertRaisesRegex(ValueError, "must be required"):
            PartitionSpec.from_model(self.env['test_new_api.partition.legacy'], {'key': 'day'})

    def test_spec_rejects_unknown_time_interval(self):
        with self.assertRaisesRegex(ValueError, "interval must be one of"):
            PartitionSpec.from_model(self.env['test_new_api.partition.event'], {'key': 'date', 'interval': 'quarter'})

    def test_spec_rejects_integer_interval_not_positive(self):
        with self.assertRaisesRegex(ValueError, "must be a positive int"):
            PartitionSpec.from_model(self.env['test_new_api.partition.idrange'], {'key': 'id', 'interval': 0})

    def test_spec_rejects_key_of_unsupported_type(self):
        with self.assertRaisesRegex(ValueError, "must be a date, datetime or integer field"):
            PartitionSpec.from_model(self.env['test_new_api.partition.event'], {'key': 'name'})

    def test_spec_rejects_negative_ahead(self):
        with self.assertRaisesRegex(ValueError, "ahead must be a non-negative int"):
            PartitionSpec.from_model(self.env['test_new_api.partition.event'], {'key': 'date', 'ahead': -1})

    def test_spec_defaults_to_a_default_partition_on_time_keys_only(self):
        self.assertTrue(
            PartitionSpec.from_model(self.env['test_new_api.partition.event']).default,
            "a date key gets a default partition unless it declares otherwise",
        )
        self.assertFalse(
            PartitionSpec.from_model(self.env['test_new_api.partition.idrange']).default,
            "an integer key gets no default partition unless it declares one",
        )

    def test_day_interval_bounds(self):
        spec = PartitionSpec('t', 'date', 'date', 'day', 1, True)
        self.assertEqual(spec.start_of(date(2026, 11, 4)), date(2026, 11, 4), "a day partition starts on its day")
        self.assertEqual(spec.next_bound(date(2026, 11, 4)), date(2026, 11, 5), "a day partition ends the next day")
        self.assertEqual(spec.partition_name(date(2026, 11, 4)), 't_p20261104', "a day partition is named by its day")

    def test_week_interval_bounds(self):
        spec = PartitionSpec('t', 'date', 'date', 'week', 1, True)
        self.assertEqual(spec.start_of(date(2026, 11, 4)), date(2026, 11, 2), "a week partition starts on Monday")
        self.assertEqual(spec.next_bound(date(2026, 11, 2)), date(2026, 11, 9), "a week partition lasts seven days")
        self.assertEqual(spec.partition_name(date(2026, 11, 2)), 't_p20261102', "a week partition is named by Monday")

    def test_month_interval_bounds(self):
        spec = PartitionSpec('t', 'date', 'date', 'month', 1, True)
        self.assertEqual(spec.start_of(date(2026, 11, 17)), date(2026, 11, 1), "a month partition starts on the 1st")
        self.assertEqual(spec.next_bound(date(2026, 12, 1)), date(2027, 1, 1), "a month partition ends on the 1st")
        self.assertEqual(spec.partition_name(date(2026, 11, 1)), 't_p202611', "a month partition is named by month")

    def test_year_interval_bounds(self):
        spec = PartitionSpec('t', 'date', 'date', 'year', 1, True)
        self.assertEqual(spec.start_of(date(2026, 11, 17)), date(2026, 1, 1), "a year partition starts on January 1st")
        self.assertEqual(spec.next_bound(date(2026, 1, 1)), date(2027, 1, 1), "a year partition lasts one year")
        self.assertEqual(spec.partition_name(date(2026, 1, 1)), 't_p2026', "a year partition is named by its year")

    def test_datetime_key_bounds_start_at_midnight(self):
        spec = PartitionSpec('t', 'at', 'datetime', 'month', 1, True)
        self.assertEqual(
            spec.start_of(datetime(2026, 11, 17, 13, 45)), datetime(2026, 11, 1),
            "a datetime partition starts at midnight of its first day",
        )

    def test_integer_key_bounds(self):
        spec = PartitionSpec('t', 'id', 'integer', 100000, 1, False)
        self.assertEqual(spec.start_of(250001), 200000, "an integer partition starts at a multiple of the interval")
        self.assertEqual(spec.next_bound(200000), 300000, "an integer partition spans one interval")
        self.assertEqual(spec.partition_name(200000), 't_p200000', "an integer partition is named by its lower bound")
