# Part of Odoo. See LICENSE file for full copyright and licensing details.
""" PostgreSQL declarative partitioning of model tables.

A model asks for a partitioned table with the ``_partition`` class attribute,
which only matters when its table is created. Everything else is decided by
what the database contains, the way the width of identifiers is: a table that
is already partitioned is managed as such whatever the model declares (it may
have been converted by hand), and an ordinary table is never converted, as
that rewrites the whole table and is a migration, not an update.

Three things differ on a partitioned table and are handled here:

* the primary key and every unique constraint must include the partition key;
* no foreign key can reference ``id`` alone, unless ``id`` is the key; the
  integrity of many2one columns pointing to such a table is kept by triggers
  that implement the same check and the same ``ondelete`` actions;
* rows only fit in an existing partition; partitions are created ahead of
  time, and an optional default partition catches the rest until the next
  maintenance moves them out.
"""
from __future__ import annotations

import datetime
import logging
import re

from dateutil.relativedelta import relativedelta

from .sql import SQL, make_identifier

_schema = logging.getLogger('odoo.schema')

SPEC_KEYS = frozenset({'by', 'key', 'interval', 'ahead', 'default'})

TIME_INTERVALS = {
    'day': relativedelta(days=1),
    'week': relativedelta(weeks=1),
    'month': relativedelta(months=1),
    'year': relativedelta(years=1),
}
TIME_SUFFIXES = {'day': '%Y%m%d', 'week': '%Y%m%d', 'month': '%Y%m', 'year': '%Y'}

FK_CHECK_FUNCTION = 'odoo_partition_fk_check'
FK_ONDELETE_FUNCTION = 'odoo_partition_fk_ondelete'
FK_ONDELETE_TRIGGER = 'odoo_partition_fk_ondelete'

FK_FUNCTIONS_SQL = r"""
CREATE OR REPLACE FUNCTION odoo_partition_fk_check() RETURNS trigger
LANGUAGE plpgsql AS $body$
DECLARE
    target regclass := to_regclass(quote_ident(TG_ARGV[0]));
    value bigint;
    found boolean;
BEGIN
    IF target IS NULL THEN
        RETURN NULL;
    END IF;
    EXECUTE format('SELECT ($1).%I', TG_ARGV[1]) INTO value USING NEW;
    IF value IS NULL THEN
        RETURN NULL;
    END IF;
    EXECUTE format('SELECT true FROM %s WHERE id = $1 FOR KEY SHARE', target) INTO found USING value;
    IF found IS NULL THEN
        RAISE EXCEPTION 'insert or update on table "%" violates foreign key constraint "%"', TG_TABLE_NAME, TG_NAME
            USING ERRCODE = 'foreign_key_violation',
                  DETAIL = format('Key (%s)=(%s) is not present in table "%s".', TG_ARGV[1], value, TG_ARGV[0]),
                  SCHEMA = TG_TABLE_SCHEMA, TABLE = TG_TABLE_NAME, COLUMN = TG_ARGV[1], CONSTRAINT = TG_NAME;
    END IF;
    RETURN NULL;
END
$body$;

CREATE OR REPLACE FUNCTION odoo_partition_fk_ondelete() RETURNS trigger
LANGUAGE plpgsql AS $body$
DECLARE
    ref record;
    blocked boolean;
BEGIN
    FOR ref IN
        SELECT t.tgrelid::regclass AS source, c.relname AS source_name, t.tgname,
               a.args[2] AS col, a.args[3] AS action
          FROM pg_trigger t
          JOIN pg_class c ON c.oid = t.tgrelid
         CROSS JOIN LATERAL (SELECT string_to_array(encode(t.tgargs, 'escape'), '\000') AS args) a
         WHERE t.tgfoid = 'odoo_partition_fk_check'::regproc
           AND t.tgparentid = 0
           AND a.args[1] = TG_TABLE_NAME
    LOOP
        IF ref.action = 'cascade' THEN
            EXECUTE format('DELETE FROM %s WHERE %I IN (SELECT id FROM odoo_old_rows)', ref.source, ref.col);
        ELSIF ref.action = 'set null' THEN
            EXECUTE format('UPDATE %s SET %I = NULL WHERE %I IN (SELECT id FROM odoo_old_rows)',
                           ref.source, ref.col, ref.col);
        ELSE
            EXECUTE format('SELECT true FROM %s WHERE %I IN (SELECT id FROM odoo_old_rows) LIMIT 1',
                           ref.source, ref.col) INTO blocked;
            IF blocked THEN
                RAISE EXCEPTION USING
                    ERRCODE = 'restrict_violation',
                    MESSAGE = format('update or delete on table "%s" violates RESTRICT setting of foreign key '
                                     || 'constraint "%s" on table "%s"', TG_TABLE_NAME, ref.tgname, ref.source_name),
                    SCHEMA = TG_TABLE_SCHEMA, TABLE = ref.source_name, COLUMN = ref.col, CONSTRAINT = ref.tgname;
            END IF;
        END IF;
    END LOOP;
    RETURN NULL;
END
$body$;
"""


class PartitionSpec:
    """ What a model declares in ``_partition``, checked against its fields.

    Only range partitioning is supported: on a date or datetime field by
    ``interval`` (``day``, ``week``, ``month``, ``year``), or on an integer
    field, ``id`` included, by a step of ``interval`` values. ``ahead`` is the
    number of partitions kept ready after the current one, and ``default``
    whether a default partition receives the rows no other partition takes.
    """

    def __init__(self, table, key, key_type, interval, ahead, default):
        self.table = table
        self.key = key
        self.key_type = key_type
        self.interval = interval
        self.ahead = ahead
        self.default = default

    @classmethod
    def from_model(cls, model, spec=None):
        """ Return the checked specification of ``model``, or of ``spec`` if
        given, and raise a ``ValueError`` explaining what is wrong otherwise.
        """
        spec = model._partition if spec is None else spec
        if not isinstance(spec, dict) or not spec.keys() <= SPEC_KEYS:
            raise ValueError(f"{model._name}: _partition must be a dict with keys among {sorted(SPEC_KEYS)}")
        if spec.get('by', 'range') != 'range':
            raise ValueError(f"{model._name}: only range partitioning is supported")
        key = spec.get('key')
        field = model._fields.get(key)
        if field is None or not field.store or not field.column_type:
            raise ValueError(f"{model._name}: partition key {key!r} must be a stored field")
        if key != 'id' and not field.required:
            raise ValueError(
                f"{model._name}: partition key {key!r} must be required, "
                "PostgreSQL puts it in the primary key and routes rows by it",
            )
        if field.type in ('date', 'datetime'):
            interval = spec.get('interval', 'month')
            if interval not in TIME_INTERVALS:
                raise ValueError(f"{model._name}: interval must be one of {sorted(TIME_INTERVALS)}")
        elif field.type in ('integer', 'many2one'):
            interval = spec.get('interval')
            if not isinstance(interval, int) or isinstance(interval, bool) or interval <= 0:
                raise ValueError(f"{model._name}: interval on an integer key must be a positive int")
        else:
            raise ValueError(f"{model._name}: partition key {key!r} must be a date, datetime or integer field")
        ahead = spec.get('ahead', 1)
        if not isinstance(ahead, int) or ahead < 0:
            raise ValueError(f"{model._name}: ahead must be a non-negative int")
        default = spec.get('default', field.type in ('date', 'datetime'))
        return cls(model._table, key, field.type, interval, ahead, bool(default))

    @property
    def is_time(self):
        return self.key_type in ('date', 'datetime')

    def start_of(self, value):
        """ Return the lower bound of the partition ``value`` belongs to. """
        if not self.is_time:
            return value - value % self.interval
        if isinstance(value, datetime.datetime):
            value = value.replace(hour=0, minute=0, second=0, microsecond=0)
        if self.interval == 'week':
            return value - datetime.timedelta(days=value.weekday())
        if self.interval == 'month':
            return value.replace(day=1)
        if self.interval == 'year':
            return value.replace(month=1, day=1)
        return value

    def next_bound(self, lower):
        if not self.is_time:
            return lower + self.interval
        return lower + TIME_INTERVALS[self.interval]

    def partition_name(self, lower):
        if self.is_time:
            suffix = lower.strftime(TIME_SUFFIXES[self.interval])
        else:
            suffix = str(lower)
        return make_identifier(f"{self.table}_p{suffix}")

    @property
    def default_name(self):
        return make_identifier(f"{self.table}_pdefault")

    def parse_bound(self, text):
        """ Convert a bound as printed by ``pg_get_expr`` to a value. """
        if text in ('MINVALUE', 'MAXVALUE'):
            return None
        text = text.strip("'")
        if self.key_type == 'date':
            return datetime.date.fromisoformat(text)
        if self.key_type == 'datetime':
            return datetime.datetime.fromisoformat(text)
        return int(text)

    def current_value(self, cr):
        """ Return the key value new rows are expected to have now. """
        if self.key_type == 'date':
            return datetime.date.today()
        if self.key_type == 'datetime':
            return datetime.datetime.now()
        if self.key == 'id':
            cr.execute(SQL(
                "SELECT COALESCE(pg_sequence_last_value(pg_get_serial_sequence(%s, 'id')::regclass), 0)",
                self.table,
            ))
        else:
            cr.execute(SQL(
                "SELECT COALESCE(max(%s), 0) FROM %s", SQL.identifier(self.key), SQL.identifier(self.table),
            ))
        return cr.fetchone()[0]


def partitioned_tables(cr, tables):
    """ Return a dict mapping the partitioned tables among ``tables`` in the
    current schema to the tuple of the columns of their partition key.
    """
    cr.execute(SQL("""
        SELECT c.relname, array_agg(a.attname ORDER BY k.ord)
          FROM pg_partitioned_table p
          JOIN pg_class c ON c.oid = p.partrelid
          JOIN pg_namespace n ON n.oid = c.relnamespace
         CROSS JOIN LATERAL unnest(p.partattrs::int2[]) WITH ORDINALITY AS k(attnum, ord)
          JOIN pg_attribute a ON a.attrelid = c.oid AND a.attnum = k.attnum
         WHERE n.nspname = current_schema AND c.relname IN %s
         GROUP BY c.relname
    """, tuple(tables)))
    return {table: tuple(columns) for table, columns in cr.fetchall()}


def needs_fk_trigger(partition_key, column):
    """ Return whether a foreign key towards ``column`` of a table partitioned
    by ``partition_key`` must be implemented with triggers: PostgreSQL only
    accepts it when the referenced column alone is the partition key.
    """
    return bool(partition_key) and partition_key != (column,)


def constraint_applicable(definition, partition_key):
    """ Return whether the SQL constraint ``definition`` can exist on a table
    partitioned by ``partition_key``: unique, primary key and exclusion
    constraints must contain every column of the key.
    """
    if not partition_key or not re.match(r'\s*(unique|primary\s+key|exclude)\b', definition, re.I):
        return True
    return all(re.search(rf'\b{re.escape(column)}\b', definition) for column in partition_key)


def list_partitions(cr, spec):
    """ Return the partitions of ``spec.table`` as ``(name, lower, upper)``,
    with ``None`` for an unbounded side, and the name of the default partition.
    """
    cr.execute(SQL("""
        SELECT c.relname, pg_get_expr(c.relpartbound, c.oid)
          FROM pg_inherits i
          JOIN pg_class c ON c.oid = i.inhrelid
          JOIN pg_class p ON p.oid = i.inhparent
          JOIN pg_namespace n ON n.oid = p.relnamespace
         WHERE p.relname = %s AND n.nspname = current_schema
    """, spec.table))
    ranges, default = [], None
    bound_re = re.compile(r"FOR VALUES FROM \((.*)\) TO \((.*)\)")
    for name, bound in cr.fetchall():
        if bound == 'DEFAULT':
            default = name
            continue
        match = bound_re.match(bound)
        if match:
            ranges.append((name, spec.parse_bound(match[1]), spec.parse_bound(match[2])))
    return ranges, default


def _overlaps(ranges, lower, upper):
    return any(
        (low is None or low < upper) and (high is None or lower < high)
        for _name, low, high in ranges
    )


def _column_names(cr, table):
    cr.execute(SQL("""
        SELECT a.attname FROM pg_attribute a
         WHERE a.attrelid = %s::regclass AND a.attnum > 0 AND NOT a.attisdropped
         ORDER BY a.attnum
    """, table))
    return [row[0] for row in cr.fetchall()]


def ensure_partitions(cr, spec):
    """ Create the default partition if ``spec`` asks for one, the partitions
    from the current one to ``spec.ahead`` after it, and a partition for every
    row waiting in the default partition, moving those rows into it. Return the
    names of the partitions created.
    """
    ranges, default = list_partitions(cr, spec)
    created = []
    if spec.default and default is None:
        default = spec.default_name
        cr.execute(SQL(
            "CREATE TABLE %s PARTITION OF %s DEFAULT",
            SQL.identifier(default), SQL.identifier(spec.table),
        ))
        created.append(default)

    lowers = []
    lower = spec.start_of(spec.current_value(cr))
    for _index in range(spec.ahead + 1):
        lowers.append(lower)
        lower = spec.next_bound(lower)
    if default is not None:
        lowers.extend(_pending_lowers(cr, spec, default))

    for lower in sorted(set(lowers)):
        upper = spec.next_bound(lower)
        if _overlaps(ranges, lower, upper):
            continue
        created.append(_create_partition(cr, spec, lower, upper, default))
        ranges.append((created[-1], lower, upper))
    if created:
        _schema.info("Table %r: created partitions %s", spec.table, ", ".join(created))
    return created


def _pending_lowers(cr, spec, default):
    if spec.is_time:
        bucket = SQL(
            "date_trunc(%s, %s)" + ("::date" if spec.key_type == 'date' else ""),
            spec.interval, SQL.identifier(spec.key),
        )
    else:
        bucket = SQL("%s - mod(%s, %s)", SQL.identifier(spec.key), SQL.identifier(spec.key), spec.interval)
    cr.execute(SQL("SELECT DISTINCT %s FROM %s", bucket, SQL.identifier(default)))
    return [row[0] for row in cr.fetchall()]


def _create_partition(cr, spec, lower, upper, default):
    """ Create the partition ``[lower, upper)`` beside the table and attach it,
    which only takes a SHARE UPDATE EXCLUSIVE lock on the partitioned table,
    moving into it first the rows the default partition holds for that range.
    """
    name = spec.partition_name(lower)
    table, key = SQL.identifier(spec.table), SQL.identifier(spec.key)
    cr.execute(SQL(
        "CREATE TABLE %s (LIKE %s INCLUDING DEFAULTS INCLUDING CONSTRAINTS)",
        SQL.identifier(name), table,
    ))
    if default is not None:
        columns = SQL(", ").join(SQL.identifier(column) for column in _column_names(cr, spec.table))
        cr.execute(SQL(
            """ WITH moved AS (
                    DELETE FROM %(default)s WHERE %(key)s >= %(lower)s AND %(key)s < %(upper)s
                    RETURNING %(columns)s
                )
                INSERT INTO %(name)s (%(columns)s) SELECT %(columns)s FROM moved """,
            default=SQL.identifier(default), key=key, lower=lower, upper=upper,
            columns=columns, name=SQL.identifier(name),
        ))
        if cr.rowcount:
            _schema.info("Table %r: moved %s rows from %r to %r", spec.table, cr.rowcount, default, name)
    cr.execute(SQL(
        "ALTER TABLE %s ATTACH PARTITION %s FOR VALUES FROM (%s) TO (%s)",
        table, SQL.identifier(name), lower, upper,
    ))
    return name


def fk_trigger_action(ondelete):
    """ Return the delete action the triggers implement for ``ondelete``:
    ``cascade`` and ``set null`` as such, anything else as ``restrict``.
    """
    ondelete = ondelete.lower()
    return ondelete if ondelete in ('cascade', 'set null') else 'restrict'


def foreign_key_triggers(cr, tables):
    """ Return the foreign keys implemented by triggers on ``tables``, as a
    dict ``{(table, column): (trigger, referenced table, ondelete)}``.
    """
    cr.execute(SQL("""
        SELECT c.relname, a.args[2], t.tgname, a.args[1], a.args[3]
          FROM pg_trigger t
          JOIN pg_class c ON c.oid = t.tgrelid
         CROSS JOIN LATERAL (SELECT string_to_array(encode(t.tgargs, 'escape'), '\\000') AS args) a
         WHERE t.tgfoid = to_regproc(%s) AND t.tgparentid = 0 AND c.relname IN %s
    """, FK_CHECK_FUNCTION, tuple(tables)))
    return {(table, column): (name, table2, ondelete) for table, column, name, table2, ondelete in cr.fetchall()}


def add_foreign_key_trigger(cr, table1, column1, table2, ondelete):
    """ Implement ``table1.column1 REFERENCES table2(id) ON DELETE ondelete``
    with triggers, and return the name of the constraint trigger.

    The check on ``table1`` locks the referenced row FOR KEY SHARE as a real
    foreign key does, and depends on the column, so that dropping the column
    drops it. The delete action is a statement trigger on ``table2`` that
    finds the referencing columns from the check triggers themselves, so it
    never refers to a table or column that no longer exists, and it does not
    fire when an update moves a row between partitions.
    """
    ondelete = fk_trigger_action(ondelete)
    cr.execute(SQL(FK_FUNCTIONS_SQL))
    name = make_identifier(f"{table1}_{column1}_pfkey")
    cr.execute(SQL(
        """ CREATE CONSTRAINT TRIGGER %s AFTER INSERT OR UPDATE OF %s ON %s
            FOR EACH ROW EXECUTE FUNCTION odoo_partition_fk_check(%s, %s, %s) """,
        SQL.identifier(name), SQL.identifier(column1), SQL.identifier(table1),
        table2, column1, ondelete,
    ))
    cr.execute(SQL(
        "SELECT 1 FROM pg_trigger WHERE tgrelid = %s::regclass AND tgname = %s",
        table2, FK_ONDELETE_TRIGGER,
    ))
    if not cr.rowcount:
        cr.execute(SQL(
            """ CREATE TRIGGER %s AFTER DELETE ON %s REFERENCING OLD TABLE AS odoo_old_rows
                FOR EACH STATEMENT EXECUTE FUNCTION odoo_partition_fk_ondelete() """,
            SQL.identifier(FK_ONDELETE_TRIGGER), SQL.identifier(table2),
        ))
    _schema.debug("Table %r: added foreign key trigger %r on %r references %r(id) ON DELETE %s",
                  table1, name, column1, table2, ondelete)
    return name


def drop_foreign_key_trigger(cr, table, name):
    cr.execute(SQL("DROP TRIGGER %s ON %s", SQL.identifier(name), SQL.identifier(table)))
    _schema.debug("Table %r: dropped foreign key trigger %r", table, name)
