# -*- coding: utf-8 -*-
from datetime import date

import psycopg2
from dateutil.relativedelta import relativedelta
from freezegun import freeze_time

from odoo.models import MetaModel
from odoo.tests import common
from odoo.tools import SQL, mute_logger
from odoo.addons.base.models.ir_model import model_xmlid, field_xmlid, selection_xmlid


def get_model_name(cls):
    name = cls._name
    if not name:
        [name] = cls._inherit if isinstance(cls._inherit, list) else [cls._inherit]
    assert isinstance(name, str)
    return name


class TestReflection(common.TransactionCase):
    """ Test the reflection into 'ir.model', 'ir.model.fields', etc. """

    def assertModelXID(self, record):
        """ Check the XML id of the given 'ir.model' record. """
        xid = model_xmlid('test_new_api', record.model)
        self.assertEqual(record, self.env.ref(xid))

    def assertFieldXID(self, record):
        """ Check the XML id of the given 'ir.model.fields' record. """
        xid = field_xmlid('test_new_api', record.model, record.name)
        self.assertEqual(record, self.env.ref(xid))

    def assertSelectionXID(self, record):
        """ Check the XML id of the given 'ir.model.fields.selection' record. """
        xid = selection_xmlid('test_new_api', record.field_id.model, record.field_id.name, record.value)
        self.assertEqual(record, self.env.ref(xid))

    def test_models_fields(self):
        """ check that all models and fields are reflected as expected. """
        # retrieve the models defined in this module, and check them
        model_names = {
            get_model_name(cls)
            for cls in MetaModel.module_to_models['test_new_api']
        }
        ir_models = self.env['ir.model'].search([('model', 'in', list(model_names))])
        self.assertEqual(len(ir_models), len(model_names))
        for ir_model in ir_models:
            with self.subTest(model=ir_model.model):
                model = self.env[ir_model.model]
                self.assertModelXID(ir_model)
                self.assertEqual(ir_model.name, model._description or False)
                self.assertEqual(ir_model.state, 'manual' if model._custom else 'base')
                self.assertEqual(ir_model.transient, bool(model._transient))
                self.assertItemsEqual(ir_model.mapped('field_id.name'), list(model._fields))
                for ir_field in ir_model.field_id:
                    with self.subTest(field=ir_field.name):
                        field = model._fields[ir_field.name]
                        self.assertFieldXID(ir_field)
                        self.assertEqual(ir_field.model, field.model_name)
                        self.assertEqual(ir_field.field_description, field.string)
                        self.assertEqual(ir_field.help, field.help or False)
                        self.assertEqual(ir_field.ttype, field.type)
                        self.assertEqual(ir_field.state, 'manual' if field.manual else 'base')
                        self.assertEqual(ir_field.index, bool(field.index))
                        self.assertEqual(ir_field.store, bool(field.store))
                        self.assertEqual(ir_field.copied, bool(field.copy))
                        self.assertEqual(ir_field.related, field.related or False)
                        self.assertEqual(ir_field.readonly, bool(field.readonly))
                        self.assertEqual(ir_field.required, bool(field.required))
                        self.assertEqual(ir_field.selectable, bool(field.search or field.store))
                        self.assertEqual(ir_field.translate, bool(field.translate))
                        if field.relational:
                            self.assertEqual(ir_field.relation, field.comodel_name)
                        if field.type == 'one2many' and field.store:
                            self.assertEqual(ir_field.relation_field, field.inverse_name)
                        if field.type == 'many2many' and field.store:
                            self.assertEqual(ir_field.relation_table, field.relation)
                            self.assertEqual(ir_field.column1, field.column1)
                            self.assertEqual(ir_field.column2, field.column2)
                            relation = self.env['ir.model.relation'].search([('name', '=', field.relation)])
                            self.assertTrue(relation)
                            self.assertIn(relation.model.model, [field.model_name, field.comodel_name])
                        if field.type == 'selection':
                            selection = [(sel.value, sel.name) for sel in ir_field.selection_ids]
                            if isinstance(field.selection, list):
                                self.assertEqual(selection, field.selection)
                            else:
                                self.assertEqual(selection, [])
                            for sel in ir_field.selection_ids:
                                self.assertSelectionXID(sel)

                field_description = field.get_description(self.env)
                if field.type in ('many2many', 'one2many'):
                    self.assertFalse(field_description['sortable'])
                elif field.store and field.column_type:
                    self.assertTrue(field_description['sortable'])


class TestSchema(common.TransactionCase):

    def get_table_data(self, tablename):
        query = ''' SELECT table_catalog, table_schema, table_name, table_type,
                           user_defined_type_catalog, user_defined_type_schema,
                           user_defined_type_name, is_insertable_into, is_typed
                    FROM information_schema.tables
                    WHERE table_name=%s '''
        self.cr.execute(query, [tablename])
        return self.cr.dictfetchone()

    def get_columns_data(self, tablename):
        query = ''' SELECT table_catalog, table_schema, table_name, column_name,
                           column_default, data_type, is_nullable, is_updatable,
                           character_maximum_length, numeric_precision,
                           numeric_precision_radix, numeric_scale,
                           datetime_precision, udt_catalog, udt_schema, udt_name
                    FROM information_schema.columns
                    WHERE table_name=%s '''
        self.cr.execute(query, [tablename])
        return {row['column_name']: row for row in self.cr.dictfetchall()}

    def get_foreign_keys(self, tablename):
        query = ''' SELECT a.table_name, a.column_name,
                           b.table_name, b.column_name, c.delete_rule
                    FROM information_schema.referential_constraints c,
                         information_schema.key_column_usage a,
                         information_schema.constraint_column_usage b
                    WHERE a.constraint_schema=c.constraint_schema
                      AND a.constraint_name=c.constraint_name
                      AND b.constraint_schema=c.constraint_schema
                      AND b.constraint_name=c.constraint_name
                      AND a.table_name=%s '''
        self.cr.execute(query, [tablename])
        return self.cr.fetchall()

    def test_00_table(self):
        """ check the database schema of a model """
        model = self.env['test_new_api.foo']
        self.assertEqual(model._table, 'test_new_api_foo')

        # retrieve schema data about that table
        table_data = self.get_table_data('test_new_api_foo')
        self.assertEqual(table_data, {
            'is_insertable_into': u'YES',
            'is_typed': u'NO',
            'table_catalog': self.cr.dbname,
            'table_name': u'test_new_api_foo',
            'table_schema': u'public',
            'table_type': u'BASE TABLE',
            'user_defined_type_catalog': None,
            'user_defined_type_name': None,
            'user_defined_type_schema': None,
        })

        # retrieve schema data about the table's columns
        columns_data = self.get_columns_data('test_new_api_foo')
        self.assertEqual(set(columns_data),
                         {'id', 'create_date', 'create_uid', 'write_date',
                          'write_uid', 'name', 'value1', 'value2', 'text'})

        # retrieve schema data about the table's foreign keys
        foreign_keys = self.get_foreign_keys('test_new_api_foo')
        self.assertItemsEqual(foreign_keys, [
            ('test_new_api_foo', 'create_uid', 'res_users', 'id', 'SET NULL'),
            ('test_new_api_foo', 'write_uid', 'res_users', 'id', 'SET NULL'),
        ])

    def test_10_boolean(self):
        """ check the database representation of a boolean field """
        model = self.env['test_new_api.message']
        columns_data = self.get_columns_data(model._table)
        self.assertEqual(columns_data['important'], {
            'character_maximum_length': None,
            'column_default': None,
            'column_name': u'important',
            'data_type': u'boolean',
            'datetime_precision': None,
            'is_nullable': u'YES',
            'is_updatable': u'YES',
            'numeric_precision': None,
            'numeric_precision_radix': None,
            'numeric_scale': None,
            'table_catalog': self.cr.dbname,
            'table_name': u'test_new_api_message',
            'table_schema': u'public',
            'udt_catalog': self.cr.dbname,
            'udt_name': u'bool',
            'udt_schema': u'pg_catalog',
        })

    def test_10_integer(self):
        """ check the database representation of an integer field """
        model = self.env['test_new_api.category']
        columns_data = self.get_columns_data(model._table)
        self.assertEqual(columns_data['color'], {
            'character_maximum_length': None,
            'column_default': None,
            'column_name': u'color',
            'data_type': u'integer',
            'datetime_precision': None,
            'is_nullable': u'YES',
            'is_updatable': u'YES',
            'numeric_precision': 32,
            'numeric_precision_radix': 2,
            'numeric_scale': 0,
            'table_catalog': self.cr.dbname,
            'table_name': u'test_new_api_category',
            'table_schema': u'public',
            'udt_catalog': self.cr.dbname,
            'udt_name': u'int4',
            'udt_schema': u'pg_catalog',
        })

    def test_10_float(self):
        """ check the database representation of a float field """
        model = self.env['test_new_api.mixed']
        columns_data = self.get_columns_data(model._table)
        self.assertEqual(columns_data['number'], {
            'character_maximum_length': None,
            'column_default': None,
            'column_name': u'number',
            'data_type': u'numeric',
            'datetime_precision': None,
            'is_nullable': u'YES',
            'is_updatable': u'YES',
            'numeric_precision': None,
            'numeric_precision_radix': 10,
            'numeric_scale': None,
            'table_catalog': self.cr.dbname,
            'table_name': u'test_new_api_mixed',
            'table_schema': u'public',
            'udt_catalog': self.cr.dbname,
            'udt_name': u'numeric',
            'udt_schema': u'pg_catalog',
        })

    def test_10_monetary(self):
        """ check the database representation of a monetary field """
        model = self.env['test_new_api.mixed']
        columns_data = self.get_columns_data(model._table)
        self.assertEqual(columns_data['amount'], {
            'character_maximum_length': None,
            'column_default': None,
            'column_name': u'amount',
            'data_type': u'numeric',
            'datetime_precision': None,
            'is_nullable': u'YES',
            'is_updatable': u'YES',
            'numeric_precision': None,
            'numeric_precision_radix': 10,
            'numeric_scale': None,
            'table_catalog': self.cr.dbname,
            'table_name': u'test_new_api_mixed',
            'table_schema': u'public',
            'udt_catalog': self.cr.dbname,
            'udt_name': u'numeric',
            'udt_schema': u'pg_catalog',
        })

    def test_10_char(self):
        """ check the database representation of a char field """
        model = self.env['res.country']
        self.assertTrue(type(model).code.required)
        self.assertEqual(type(model).code.size, 2)
        columns_data = self.get_columns_data(model._table)
        self.assertEqual(columns_data['code'], {
            'character_maximum_length': 2,
            'column_default': None,
            'column_name': u'code',
            'data_type': u'character varying',
            'datetime_precision': None,
            'is_nullable': u'NO',
            'is_updatable': u'YES',
            'numeric_precision': None,
            'numeric_precision_radix': None,
            'numeric_scale': None,
            'table_catalog': self.cr.dbname,
            'table_name': u'res_country',
            'table_schema': u'public',
            'udt_catalog': self.cr.dbname,
            'udt_name': u'varchar',
            'udt_schema': u'pg_catalog',
        })

        model = self.env['test_new_api.message']
        self.assertFalse(type(model).name.required)
        columns_data = self.get_columns_data(model._table)
        self.assertEqual(columns_data['name'], {
            'character_maximum_length': None,
            'column_default': None,
            'column_name': u'name',
            'data_type': u'character varying',
            'datetime_precision': None,
            'is_nullable': u'YES',
            'is_updatable': u'YES',
            'numeric_precision': None,
            'numeric_precision_radix': None,
            'numeric_scale': None,
            'table_catalog': self.cr.dbname,
            'table_name': u'test_new_api_message',
            'table_schema': u'public',
            'udt_catalog': self.cr.dbname,
            'udt_name': u'varchar',
            'udt_schema': u'pg_catalog',
        })

        model = self.env['test_new_api.category']
        self.assertTrue(type(model).name.required)
        columns_data = self.get_columns_data(model._table)
        self.assertEqual(columns_data['name'], {
            'character_maximum_length': None,
            'column_default': None,
            'column_name': u'name',
            'data_type': u'character varying',
            'datetime_precision': None,
            'is_nullable': u'NO',
            'is_updatable': u'YES',
            'numeric_precision': None,
            'numeric_precision_radix': None,
            'numeric_scale': None,
            'table_catalog': self.cr.dbname,
            'table_name': u'test_new_api_category',
            'table_schema': u'public',
            'udt_catalog': self.cr.dbname,
            'udt_name': u'varchar',
            'udt_schema': u'pg_catalog',
        })

    def test_10_text(self):
        """ check the database representation of a text field """
        model = self.env['test_new_api.message']
        columns_data = self.get_columns_data(model._table)
        self.assertEqual(columns_data['body'], {
            'character_maximum_length': None,
            'column_default': None,
            'column_name': u'body',
            'data_type': u'text',
            'datetime_precision': None,
            'is_nullable': u'YES',
            'is_updatable': u'YES',
            'numeric_precision': None,
            'numeric_precision_radix': None,
            'numeric_scale': None,
            'table_catalog': self.cr.dbname,
            'table_name': u'test_new_api_message',
            'table_schema': u'public',
            'udt_catalog': self.cr.dbname,
            'udt_name': u'text',
            'udt_schema': u'pg_catalog',
        })

    def test_10_html(self):
        """ check the database representation of an html field """
        model = self.env['test_new_api.mixed']
        columns_data = self.get_columns_data(model._table)
        self.assertEqual(columns_data['comment1'], {
            'character_maximum_length': None,
            'column_default': None,
            'column_name': u'comment1',
            'data_type': u'text',
            'datetime_precision': None,
            'is_nullable': u'YES',
            'is_updatable': u'YES',
            'numeric_precision': None,
            'numeric_precision_radix': None,
            'numeric_scale': None,
            'table_catalog': self.cr.dbname,
            'table_name': u'test_new_api_mixed',
            'table_schema': u'public',
            'udt_catalog': self.cr.dbname,
            'udt_name': u'text',
            'udt_schema': u'pg_catalog',
        })

    def test_10_date(self):
        """ check the database representation of a date field """
        model = self.env['test_new_api.mixed']
        columns_data = self.get_columns_data(model._table)
        self.assertEqual(columns_data['date'], {
            'character_maximum_length': None,
            'column_default': None,
            'column_name': u'date',
            'data_type': u'date',
            'datetime_precision': 0,
            'is_nullable': u'YES',
            'is_updatable': u'YES',
            'numeric_precision': None,
            'numeric_precision_radix': None,
            'numeric_scale': None,
            'table_catalog': self.cr.dbname,
            'table_name': u'test_new_api_mixed',
            'table_schema': u'public',
            'udt_catalog': self.cr.dbname,
            'udt_name': u'date',
            'udt_schema': u'pg_catalog',
        })

    def test_10_datetime(self):
        """ check the database representation of a datetime field """
        model = self.env['ir.property']
        columns_data = self.get_columns_data(model._table)
        self.assertEqual(columns_data['value_datetime'], {
            'character_maximum_length': None,
            'column_default': None,
            'column_name': u'value_datetime',
            'data_type': u'timestamp without time zone',
            'datetime_precision': 6,
            'is_nullable': u'YES',
            'is_updatable': u'YES',
            'numeric_precision': None,
            'numeric_precision_radix': None,
            'numeric_scale': None,
            'table_catalog': self.cr.dbname,
            'table_name': u'ir_property',
            'table_schema': u'public',
            'udt_catalog': self.cr.dbname,
            'udt_name': u'timestamp',
            'udt_schema': u'pg_catalog',
        })

        model = self.env['test_new_api.mixed']
        columns_data = self.get_columns_data(model._table)
        self.assertEqual(columns_data['create_date'], {
            'character_maximum_length': None,
            'column_default': None,
            'column_name': u'create_date',
            'data_type': u'timestamp without time zone',
            'datetime_precision': 6,
            'is_nullable': u'YES',
            'is_updatable': u'YES',
            'numeric_precision': None,
            'numeric_precision_radix': None,
            'numeric_scale': None,
            'table_catalog': self.cr.dbname,
            'table_name': u'test_new_api_mixed',
            'table_schema': u'public',
            'udt_catalog': self.cr.dbname,
            'udt_name': u'timestamp',
            'udt_schema': u'pg_catalog',
        })

    def test_10_selection(self):
        """ check the database representation of a selection field """
        model = self.env['test_new_api.mixed']
        columns_data = self.get_columns_data(model._table)
        self.assertEqual(columns_data['lang'], {
            'character_maximum_length': None,
            'column_default': None,
            'column_name': u'lang',
            'data_type': u'character varying',
            'datetime_precision': None,
            'is_nullable': u'YES',
            'is_updatable': u'YES',
            'numeric_precision': None,
            'numeric_precision_radix': None,
            'numeric_scale': None,
            'table_catalog': self.cr.dbname,
            'table_name': u'test_new_api_mixed',
            'table_schema': u'public',
            'udt_catalog': self.cr.dbname,
            'udt_name': u'varchar',
            'udt_schema': u'pg_catalog',
        })

    def test_10_reference(self):
        """ check the database representation of a reference field """
        model = self.env['test_new_api.mixed']
        columns_data = self.get_columns_data(model._table)
        self.assertEqual(columns_data['reference'], {
            'character_maximum_length': None,
            'column_default': None,
            'column_name': u'reference',
            'data_type': u'character varying',
            'datetime_precision': None,
            'is_nullable': u'YES',
            'is_updatable': u'YES',
            'numeric_precision': None,
            'numeric_precision_radix': None,
            'numeric_scale': None,
            'table_catalog': self.cr.dbname,
            'table_name': u'test_new_api_mixed',
            'table_schema': u'public',
            'udt_catalog': self.cr.dbname,
            'udt_name': u'varchar',
            'udt_schema': u'pg_catalog',
        })

    def test_10_many2one(self):
        """ check the database representation of a many2one field """
        model = self.env['test_new_api.mixed']
        columns_data = self.get_columns_data(model._table)
        self.assertEqual(columns_data['currency_id'], {
            'character_maximum_length': None,
            'column_default': None,
            'column_name': u'currency_id',
            'data_type': u'integer',
            'datetime_precision': None,
            'is_nullable': u'YES',
            'is_updatable': u'YES',
            'numeric_precision': 32,
            'numeric_precision_radix': 2,
            'numeric_scale': 0,
            'table_catalog': self.cr.dbname,
            'table_name': u'test_new_api_mixed',
            'table_schema': u'public',
            'udt_catalog': self.cr.dbname,
            'udt_name': u'int4',
            'udt_schema': u'pg_catalog',
        })
        foreign_keys = self.get_foreign_keys(model._table)
        self.assertIn(
            ('test_new_api_mixed', 'currency_id', 'res_currency', 'id', 'SET NULL'),
            foreign_keys,
        )

    def test_10_many2many(self):
        """ check the database representation of a many2many field """
        model = self.env['test_new_api.discussion']
        field = type(model).categories
        comodel = self.env[field.comodel_name]
        self.assertTrue(field.relation)
        self.assertTrue(field.column1)
        self.assertTrue(field.column2)

        columns_data = self.get_columns_data(model._table)
        self.assertNotIn('categories', columns_data)

        table_data = self.get_table_data(field.relation)
        self.assertEqual(table_data, {
            'is_insertable_into': u'YES',
            'is_typed': u'NO',
            'table_catalog': self.cr.dbname,
            'table_name': u'test_new_api_discussion_category',
            'table_schema': u'public',
            'table_type': u'BASE TABLE',
            'user_defined_type_catalog': None,
            'user_defined_type_name': None,
            'user_defined_type_schema': None,
        })

        columns_data = self.get_columns_data(field.relation)
        self.assertEqual(columns_data, {
            field.column1: {
                'character_maximum_length': None,
                'column_default': None,
                'column_name': u'discussion',
                'data_type': u'integer',
                'datetime_precision': None,
                'is_nullable': u'NO',
                'is_updatable': u'YES',
                'numeric_precision': 32,
                'numeric_precision_radix': 2,
                'numeric_scale': 0,
                'table_catalog': self.cr.dbname,
                'table_name': u'test_new_api_discussion_category',
                'table_schema': u'public',
                'udt_catalog': self.cr.dbname,
                'udt_name': u'int4',
                'udt_schema': u'pg_catalog',
            },
            field.column2: {
                'character_maximum_length': None,
                'column_default': None,
                'column_name': u'category',
                'data_type': u'integer',
                'datetime_precision': None,
                'is_nullable': u'NO',
                'is_updatable': u'YES',
                'numeric_precision': 32,
                'numeric_precision_radix': 2,
                'numeric_scale': 0,
                'table_catalog': self.cr.dbname,
                'table_name': u'test_new_api_discussion_category',
                'table_schema': u'public',
                'udt_catalog': self.cr.dbname,
                'udt_name': u'int4',
                'udt_schema': u'pg_catalog'
            },
        })

        foreign_keys = self.get_foreign_keys(field.relation)
        self.assertItemsEqual(foreign_keys, [
            (field.relation, field.column1, model._table, 'id', 'CASCADE'),
            (field.relation, field.column2, comodel._table, 'id', 'CASCADE'),
        ])

    def test_20_unique_indexes(self):
        """ Test uniqueness of indexes:
        - test_new_api.order.line_short_field_name
        - test_new_api.order.line.short_field_name
        """
        tablenames = ('test_new_api_order', 'test_new_api_order_line')
        self.env.cr.execute("""
            SELECT tablename
            FROM pg_indexes
            WHERE tablename IN %s AND indexdef LIKE %s
        """, [tablenames, '%short_field_name%'])
        tables = {table for table, in self.env.cr.fetchall()}
        self.assertEqual(tables, {'test_new_api_order', 'test_new_api_order_line'})

    def test_21_too_long_indexes(self):
        """ Test too long indexes name:

        Both indexes share same truncated name
        'test_new_api_order_line__very_very_very_very_very_long_field_nam'
        if no strategy is done to avoid duplicate too long index names

        -  test_new_api.order.line.very_very_very_very_very_long_field_name_1
        -> test_new_api_order_line__very_very_very_very_very_long_field_name_1_index
        => test_new_api_order_line__very_very_very_very_very_long_ea4b39c9

        -  test_new_api.order.line.very_very_very_very_very_long_field_name_2
        -> test_new_api_order_line__very_very_very_very_very_long_field_name_2_index
        => test_new_api_order_line__very_very_very_very_very_long_dba32354
        """
        self.env.cr.execute("""
            SELECT COUNT(*)
            FROM pg_indexes
            WHERE tablename = 'test_new_api_order_line' AND indexdef LIKE %s
        """, ['%very_very_very_very_long_field_name%'])
        nb_field_index, = self.env.cr.fetchone()
        self.assertEqual(nb_field_index, 2)


class TestPartitionedTables(common.TransactionCase):

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.this_month = date.today().replace(day=1)
        cls.Event = cls.env['test_new_api.partition.event']
        cls.Legacy = cls.env['test_new_api.partition.legacy']
        cls.Reference = cls.env['test_new_api.partition.reference']

    def test_declared_model_gets_a_partitioned_table(self):
        self.assertEqual(self.relkind(self.Event._table), 'p', "the table of a declared model is partitioned")
        self.assertEqual(
            self.primary_key_columns(self.Event._table), ['date', 'id'],
            "the primary key of a table partitioned by date includes the date",
        )

    def test_install_creates_current_ahead_and_default_partitions(self):
        self.assertEqual(
            self.partitions(self.Event._table),
            {
                self.month_partition(0), self.month_partition(1), self.month_partition(2),
                'test_new_api_partition_event_pdefault',
            },
            "install creates this month, two months ahead and the default partition",
        )

    def test_create_routes_rows_to_their_partition(self):
        event = self.Event.create({'name': 'now', 'date': self.months_after(0)})
        self.assertEqual(
            self.partition_of(event), self.month_partition(0),
            "a row of this month is stored in the partition of this month",
        )
        event = self.Event.create({'name': 'later', 'date': self.months_after(24)})
        self.assertEqual(
            self.partition_of(event), 'test_new_api_partition_event_pdefault',
            "a row beyond the existing partitions is stored in the default partition",
        )

    def test_update_moves_default_rows_to_their_partition(self):
        event = self.Event.create({'name': 'later', 'date': self.months_after(24)})
        self.assertIsNone(self.update_models(self.Event._name), "the update of a declared model succeeds")
        self.assertEqual(
            self.partition_of(event), self.month_partition(24),
            "the update moves a row out of the default partition into a partition of its own",
        )
        self.env.invalidate_all()
        self.assertEqual(event.name, 'later', "the moved row keeps its id and is still readable")

    def test_update_creates_partitions_ahead_of_today(self):
        with freeze_time(self.months_after(6)):
            self.assertIsNone(self.update_models(self.Event._name), "the update of a declared model succeeds")
        self.assertLessEqual(
            {self.month_partition(6), self.month_partition(7), self.month_partition(8)},
            self.partitions(self.Event._table),
            "the update creates the partitions of the current month and two months ahead",
        )

    def test_update_never_converts_an_ordinary_table(self):
        self.unpartition_event_by_hand()
        with self.assertLogs('odoo.schema', 'INFO') as logs:
            self.assertIsNone(self.update_models(self.Event._name), "the update of a declared model succeeds")
        self.assertEqual(self.relkind(self.Event._table), 'r', "an ordinary table stays ordinary")
        self.assertIn(
            "partitions are not maintained", "\n".join(logs.output),
            "the update reports that the declared partitioning is not applied",
        )

    def test_write_on_key_moves_row_and_keeps_references(self):
        event = self.Event.create({'name': 'moving', 'date': self.months_after(0)})
        reference = self.Reference.create({'event_id': event.id})
        event.date = self.months_after(1)
        self.assertEqual(
            self.partition_of(event), self.month_partition(1),
            "writing the key moves the row to the partition of its new date",
        )
        self.env.invalidate_all()
        self.assertEqual(
            reference.exists().event_id, event,
            "moving a row between partitions does not fire the ondelete of its references",
        )

    def test_unique_constraint_including_key_is_enforced(self):
        self.Event.create({'name': 'twice', 'date': self.months_after(0)})
        with self.assertRaises(psycopg2.errors.UniqueViolation), mute_logger('odoo.sql_db'), self.cr.savepoint():
            self.Event.create({'name': 'twice', 'date': self.months_after(0)})

    def test_unlink_cascades_to_referencing_rows(self):
        event = self.Event.create({'name': 'target', 'date': self.months_after(0)})
        reference = self.Reference.create({'event_id': event.id})
        event.unlink()
        self.env.invalidate_all()
        self.assertFalse(reference.exists(), "ondelete cascade removes the referencing row")

    def test_unlink_sets_null_on_referencing_rows(self):
        event = self.Event.create({'name': 'target', 'date': self.months_after(0)})
        reference = self.Reference.create({'event_set_null_id': event.id})
        event.unlink()
        self.env.invalidate_all()
        self.assertFalse(reference.event_set_null_id, "ondelete set null empties the referencing column")

    def test_unlink_restricted_by_referencing_rows(self):
        event = self.Event.create({'name': 'target', 'date': self.months_after(0)})
        self.Reference.create({'event_restrict_id': event.id})
        with self.assertRaises(psycopg2.errors.RestrictViolation), mute_logger('odoo.sql_db'), self.cr.savepoint():
            event.unlink()

    def test_reference_to_missing_record_is_rejected(self):
        event = self.Event.create({'name': 'target', 'date': self.months_after(0)})
        with self.assertRaises(psycopg2.errors.ForeignKeyViolation), mute_logger('odoo.sql_db'), self.cr.savepoint():
            self.Reference.create({'event_id': event.id + 1000})

    def test_many2many_rows_removed_with_partitioned_record(self):
        event = self.Event.create({'name': 'target', 'date': self.months_after(0)})
        self.Reference.create({'event_ids': [event.id]})
        self.env.flush_all()
        event.unlink()
        self.cr.execute(SQL(
            "SELECT count(*) FROM test_new_api_partition_event_reference_rel WHERE event_id = %s", event.id,
        ))
        self.assertEqual(self.cr.fetchone()[0], 0, "the relation rows of a deleted partitioned record are removed")

    def test_foreign_key_trigger_is_reflected_as_constraint(self):
        constraint = self.env['ir.model.constraint'].search([
            ('name', '=', 'test_new_api_partition_reference_event_id_pfkey'),
        ])
        self.assertEqual(
            constraint.mapped('type'), ['f'],
            "the trigger implementing a many2one to a table partitioned by date is reflected as a foreign key",
        )

    def test_update_changes_the_action_of_a_foreign_key_trigger(self):
        self.cr.execute(SQL("""
            DROP TRIGGER test_new_api_partition_reference_event_id_pfkey ON test_new_api_partition_reference;
            CREATE CONSTRAINT TRIGGER test_new_api_partition_reference_event_id_pfkey
                AFTER INSERT OR UPDATE OF event_id ON test_new_api_partition_reference FOR EACH ROW
                EXECUTE FUNCTION odoo_partition_fk_check('test_new_api_partition_event', 'event_id', 'restrict')
        """))
        self.assertIsNone(
            self.update_models(self.Event._name, self.Reference._name), "the update of the referencing model succeeds",
        )
        event = self.Event.create({'name': 'target', 'date': self.months_after(0)})
        reference = self.Reference.create({'event_id': event.id})
        event.unlink()
        self.env.invalidate_all()
        self.assertFalse(reference.exists(), "the update restores the ondelete cascade the field declares")

    def test_update_turns_foreign_key_trigger_into_foreign_key_on_ordinary_table(self):
        self.unpartition_event_by_hand()
        self.assertIsNone(
            self.update_models(self.Event._name, self.Reference._name), "the update of the referencing model succeeds",
        )
        self.assertEqual(
            self.foreign_key_kinds(self.Reference._table, self.Event._table), ['f', 'f', 'f'],
            "the many2one fields towards an ordinary table are real foreign keys again",
        )

    def test_update_of_hand_partitioned_table_keeps_it(self):
        self.partition_by_hand(self.Legacy._table, 'day')
        self.assertIsNone(
            self.update_models(self.Legacy._name), "the update of a model whose table is partitioned succeeds",
        )
        self.assertEqual(self.relkind(self.Legacy._table), 'p', "the update leaves the table partitioned")

    def test_update_keeps_not_null_on_partition_key(self):
        self.partition_by_hand(self.Legacy._table, 'day')
        with self.assertLogs('odoo.schema', 'WARNING') as logs:
            self.assertIsNone(
                self.update_models(self.Legacy._name), "the update of a model whose table is partitioned succeeds",
            )
        self.assertFalse(
            self.column_is_nullable(self.Legacy._table, 'day'),
            "the update keeps NOT NULL on the partition key of a field that is not required",
        )
        self.assertIn(
            "column 'day' is in the partition key", "\n".join(logs.output),
            "the update asks to declare the partition key required",
        )

    def test_update_skips_unique_constraint_without_key(self):
        self.partition_by_hand(self.Legacy._table, 'day')
        with self.assertLogs('odoo.schema', 'WARNING') as logs:
            self.assertIsNone(
                self.update_models(self.Legacy._name), "the update of a model whose table is partitioned succeeds",
            )
        self.assertNotIn(
            'test_new_api_partition_legacy_code_uniq', self.constraint_names(self.Legacy._table),
            "the partitioned table has no unique constraint without its partition key",
        )
        self.assertIn(
            "test_new_api_partition_legacy_code_uniq", "\n".join(logs.output),
            "the update reports the unique constraint it does not create",
        )

    def test_update_replaces_foreign_keys_to_hand_partitioned_table_by_triggers(self):
        self.partition_by_hand(self.Legacy._table, 'day')
        self.cr.execute(SQL("""
            ALTER TABLE test_new_api_partition_legacy_hist ADD UNIQUE (id);
            ALTER TABLE test_new_api_partition_reference ADD FOREIGN KEY (legacy_id)
                REFERENCES test_new_api_partition_legacy_hist (id) ON DELETE SET NULL;
        """))
        self.assertIsNone(
            self.update_models(self.Legacy._name, self.Reference._name),
            "the update of a model referencing a partitioned table succeeds",
        )
        legacy = self.Legacy.create({'day': self.months_after(1)})
        reference = self.Reference.create({'legacy_id': legacy.id})
        self.env.flush_all()
        self.assertEqual(
            self.foreign_key_kinds(self.Reference._table, 'test_new_api_partition_legacy_hist'), [],
            "no foreign key is left pointing to the old table, now one of the partitions",
        )
        legacy.unlink()
        self.env.invalidate_all()
        self.assertFalse(reference.legacy_id, "ondelete set null applies to a row of a new partition")

    def test_update_adds_outgoing_foreign_key_to_hand_partitioned_table(self):
        self.partition_by_hand(self.Legacy._table, 'day')
        self.assertIsNone(
            self.update_models(self.Legacy._name), "the update of a model whose table is partitioned succeeds",
        )
        partner = self.env['res.partner'].create({'name': 'target'})
        legacy = self.Legacy.create({'day': self.months_after(1), 'partner_id': partner.id})
        partner.unlink()
        self.env.invalidate_all()
        self.assertFalse(legacy.partner_id, "a many2one from a partitioned table keeps its ondelete set null")

    def test_many2one_to_id_partitioned_table_is_a_real_foreign_key(self):
        idrange_table = self.env['test_new_api.partition.idrange']._table
        self.assertEqual(self.relkind(idrange_table), 'p', "the table of a model declared by id is partitioned")
        self.assertEqual(
            self.primary_key_columns(idrange_table), ['id'],
            "a table partitioned by id keeps id alone as primary key",
        )
        self.assertEqual(
            self.foreign_key_kinds(self.Reference._table, idrange_table), ['f'],
            "a many2one towards a table partitioned by id is a real foreign key",
        )

    def test_update_keeps_foreign_key_to_id_partitioned_table(self):
        idrange = self.env['test_new_api.partition.idrange']
        before = self.foreign_key_oids(self.Reference._table, idrange._table)
        self.assertIsNone(
            self.update_models(idrange._name, self.Reference._name), "the update of the referencing model succeeds",
        )
        self.assertEqual(
            self.foreign_key_oids(self.Reference._table, idrange._table), before,
            "the update leaves the foreign key towards a table partitioned by id untouched",
        )

    def test_maintain_ignores_model_without_declaration(self):
        self.assertEqual(
            self.Legacy.partition_maintain(), [], "maintenance does nothing on a model that declares no partitioning",
        )

    def relkind(self, table):
        self.cr.execute(SQL(
            "SELECT relkind FROM pg_class WHERE relname = %s AND relnamespace = current_schema::regnamespace", table,
        ))
        return self.cr.fetchone()[0]

    def partitions(self, table):
        self.cr.execute(SQL("SELECT inhrelid::regclass::text FROM pg_inherits WHERE inhparent = %s::regclass", table))
        return {row[0] for row in self.cr.fetchall()}

    def partition_of(self, record):
        record.flush_recordset()
        self.cr.execute(SQL(
            "SELECT tableoid::regclass::text FROM %s WHERE id = %s", SQL.identifier(record._table), record.id,
        ))
        return self.cr.fetchone()[0]

    def primary_key_columns(self, table):
        self.cr.execute(SQL(
            """ SELECT array_agg(a.attname::text ORDER BY a.attname)
                  FROM pg_constraint c
                  JOIN pg_attribute a ON a.attrelid = c.conrelid AND a.attnum = ANY(c.conkey)
                 WHERE c.conrelid = %s::regclass AND c.contype = 'p' """,
            table,
        ))
        return self.cr.fetchone()[0]

    def constraint_names(self, table):
        self.cr.execute(SQL("SELECT conname FROM pg_constraint WHERE conrelid = %s::regclass", table))
        return {row[0] for row in self.cr.fetchall()}

    def foreign_key_kinds(self, table, referenced_table):
        self.cr.execute(SQL(
            """ SELECT contype FROM pg_constraint
                 WHERE conrelid = %s::regclass AND confrelid = %s::regclass AND conparentid = 0 """,
            table, referenced_table,
        ))
        return [row[0] for row in self.cr.fetchall()]

    def foreign_key_oids(self, table, referenced_table):
        self.cr.execute(SQL(
            """ SELECT oid FROM pg_constraint
                 WHERE conrelid = %s::regclass AND confrelid = %s::regclass AND conparentid = 0 """,
            table, referenced_table,
        ))
        return [row[0] for row in self.cr.fetchall()]

    def column_is_nullable(self, table, column):
        self.cr.execute(SQL(
            "SELECT is_nullable FROM information_schema.columns WHERE table_name = %s AND column_name = %s",
            table, column,
        ))
        return self.cr.fetchone()[0] == 'YES'

    def months_after(self, months):
        return self.this_month + relativedelta(months=months)

    def month_partition(self, months):
        return f"test_new_api_partition_event_p{self.months_after(months):%Y%m}"

    def update_models(self, *model_names):
        try:
            with mute_logger('odoo.sql_db'), self.cr.savepoint():
                self.registry.init_models(self.cr, list(model_names), {'module': 'test_new_api'}, install=False)
        except psycopg2.Error as error:
            return error
        return None

    def partition_by_hand(self, table, column):
        self.cr.execute(SQL(
            """
            ALTER TABLE %(table)s RENAME TO %(hist)s;
            ALTER TABLE %(hist)s DROP CONSTRAINT %(pkey)s CASCADE;
            ALTER TABLE %(hist)s ALTER COLUMN %(column)s SET NOT NULL;
            CREATE TABLE %(table)s (LIKE %(hist)s INCLUDING DEFAULTS INCLUDING COMMENTS)
                PARTITION BY RANGE (%(column)s);
            ALTER TABLE %(table)s ADD CONSTRAINT %(pkey)s PRIMARY KEY (id, %(column)s);
            ALTER SEQUENCE %(sequence)s OWNED BY %(table)s.id;
            ALTER TABLE %(table)s ATTACH PARTITION %(hist)s FOR VALUES FROM (MINVALUE) TO (%(bound)s);
            CREATE TABLE %(current)s PARTITION OF %(table)s FOR VALUES FROM (%(bound)s) TO (MAXVALUE);
            """,
            table=SQL.identifier(table),
            hist=SQL.identifier(f'{table}_hist'),
            current=SQL.identifier(f'{table}_current'),
            column=SQL.identifier(column),
            pkey=SQL.identifier(f'{table}_pkey'),
            sequence=SQL.identifier(f'{table}_id_seq'),
            bound=self.months_after(1),
        ))

    def unpartition_event_by_hand(self):
        table = self.Event._table
        self.cr.execute(SQL(
            """
            ALTER TABLE %(table)s RENAME TO %(old)s;
            ALTER INDEX %(pkey)s RENAME TO %(old_pkey)s;
            ALTER INDEX %(unique)s RENAME TO %(old_unique)s;
            CREATE TABLE %(table)s (LIKE %(old)s INCLUDING DEFAULTS INCLUDING COMMENTS, PRIMARY KEY (id));
            ALTER SEQUENCE %(sequence)s OWNED BY %(table)s.id;
            """,
            table=SQL.identifier(table),
            old=SQL.identifier(f'{table}_old'),
            pkey=SQL.identifier(f'{table}_pkey'),
            old_pkey=SQL.identifier(f'{table}_old_pkey'),
            unique=SQL.identifier(f'{table}_name_date_uniq'),
            old_unique=SQL.identifier(f'{table}_old_name_date_uniq'),
            sequence=SQL.identifier(f'{table}_id_seq'),
        ))
