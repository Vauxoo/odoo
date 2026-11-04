import uuid

from psycopg2 import IntegrityError

from odoo import Command
from odoo.tests import common
from odoo.tools import mute_logger


class TestUuidIds(common.TransactionCase):

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.partner = cls.env['res.partner'].create({'name': 'UUID partner'})
        cls.ref = cls.env['test_uuid_ids.ref'].create({'name': 'Integer ref'})
        cls.doc = cls.env['test_uuid_ids.doc'].create({'name': 'Doc A'})
        cls.other_doc = cls.env['test_uuid_ids.doc'].create({'name': 'Doc B'})
        cls.line = cls.env['test_uuid_ids.line'].create({
            'name': 'Line 1',
            'doc_id': cls.doc.id,
            'partner_id': cls.partner.id,
            'tag_ids': [Command.set([cls.other_doc.id])],
            'ref_ids': [Command.set([cls.ref.id])],
        })

    def test_uuid_model_has_uuidv7_ids(self):
        self.assertEqual(self._get_column_type('test_uuid_ids_doc', 'id'), ('uuid', 'uuidv7()'),
                         "uuid model: id column is uuid defaulted by uuidv7()")
        self.assertEqual(self._get_column_type('test_uuid_ids_ref', 'id')[0], 'int4',
                         "integer model: id column stays int4")
        self.assertEqual(uuid.UUID(self.doc.id).version, 7, "uuid model: created id is a UUIDv7")
        self.assertGreater(self.other_doc.id, self.doc.id, "uuid model: a later record has a greater id")

        values = self.line.read(['doc_id', 'partner_id', 'tag_ids', 'ref_ids'])[0]
        self.assertIsInstance(values['id'], str, "read: id of a uuid model is text")
        self.assertEqual(values['doc_id'], (self.doc.id, 'Doc A'), "read: uuid many2one is (uuid, name)")
        self.assertEqual(values['partner_id'], (self.partner.id, 'UUID partner'),
                         "read: integer many2one is (int, name)")
        self.assertEqual(values['tag_ids'], [self.other_doc.id], "read: uuid many2many lists uuids")
        self.assertEqual(values['ref_ids'], [self.ref.id], "read: integer many2many lists ints")

        self.assertEqual(self.env['test_uuid_ids.doc'].name_search('Doc A'), [(self.doc.id, 'Doc A')],
                         "name_search: pairs carry the uuid")

    def test_many2one_column_follows_comodel_id_type(self):
        self.assertEqual(self._get_column_type('test_uuid_ids_line', 'doc_id')[0], 'uuid',
                         "uuid model -> uuid model: many2one column is uuid")
        self.assertEqual(self._get_column_type('test_uuid_ids_line', 'partner_id')[0], 'int4',
                         "uuid model -> integer model: many2one column is int4")
        self.assertEqual(self._get_column_type('test_uuid_ids_ref', 'doc_id')[0], 'uuid',
                         "integer model -> uuid model: many2one column is uuid")

    def test_many2many_relation_columns_follow_each_side(self):
        self.assertEqual(self._get_column_type('test_uuid_ids_line_doc_rel', 'line_id')[0], 'uuid',
                         "uuid <-> uuid relation: column1 is uuid")
        self.assertEqual(self._get_column_type('test_uuid_ids_line_doc_rel', 'doc_id')[0], 'uuid',
                         "uuid <-> uuid relation: column2 is uuid")
        self.assertEqual(self._get_column_type('test_uuid_ids_line_ref_rel', 'line_id')[0], 'uuid',
                         "uuid <-> integer relation: uuid side is uuid")
        self.assertEqual(self._get_column_type('test_uuid_ids_line_ref_rel', 'ref_id')[0], 'int4',
                         "uuid <-> integer relation: integer side is int4")

    def test_existing_integer_table_keeps_integer_ids(self):
        legacy = self.env['test_uuid_ids.legacy'].create({'name': 'Legacy'})
        self.assertEqual(self._get_column_type('test_uuid_ids_legacy', 'id')[0], 'int4',
                         "uuid declared on an existing int4 table: id column kept")
        self.assertIsInstance(legacy.id, int, "uuid declared on an existing int4 table: ids stay integers")
        self.assertEqual(self._get_column_type('test_uuid_ids_doc', 'legacy_id')[0], 'int4',
                         "uuid declared on an existing int4 table: many2one columns to it are int4")

    def test_existing_uuid_column_is_not_converted(self):
        self.assertEqual(self._get_column_type('test_uuid_ids_legacy', 'code')[0], 'uuid',
                         "char field on an existing uuid column: column kept as uuid")

    def test_browse_canonicalizes_uuid_text(self):
        upper = self.env['test_uuid_ids.doc'].browse(str(self.doc.id).upper())
        self.assertEqual(upper, self.doc, "browse of an upper-case uuid is the same record")
        self.assertEqual(upper.name, 'Doc A', "browse of an upper-case uuid reads the record")
        hexa = self.env['test_uuid_ids.doc'].browse([str(self.other_doc.id).replace('-', '')])
        self.assertEqual(hexa, self.other_doc, "browse of a list with a hyphen-less uuid is the same record")

    def test_new_record_keeps_new_ids(self):
        draft = self.env['test_uuid_ids.doc'].new({'name': 'Draft', 'line_ids': [Command.create({'name': 'L'})]})
        self.assertFalse(draft.id, "new record of a uuid model has a new id")
        self.assertEqual(draft.line_ids.doc_id, draft, "new line of a new uuid record points to it")

    def test_many2one_accepts_uuid_text(self):
        self.ref.write({'doc_id': str(self.other_doc.id).upper()})
        self.assertEqual(self.ref.doc_id, self.other_doc, "integer model: many2one written with uuid text")
        self.assertEqual(self.other_doc.ref_ids, self.ref, "integer model: inverse one2many sees the record")

        self.line.write({'doc_id': str(self.other_doc.id)})
        self.assertEqual(self.line.doc_id, self.other_doc, "uuid model: many2one written with uuid text")

        copy = self.line.copy()
        self.assertNotEqual(copy.id, self.line.id, "copy: gets a new uuid")
        self.assertEqual(copy.doc_id, self.other_doc, "copy: keeps the uuid many2one")
        self.assertEqual(copy.partner_id, self.partner, "copy: keeps the integer many2one")
        self.assertEqual(copy.tag_ids, self.other_doc, "copy: keeps the uuid many2many")
        self.assertEqual(copy.ref_ids, self.ref, "copy: keeps the integer many2many")

    def test_many2one_default_with_uuid_text(self):
        line_model = self.env['test_uuid_ids.line'].with_context(default_doc_id=str(self.doc.id).upper())
        self.assertEqual(line_model.default_get(['doc_id']), {'doc_id': self.doc.id},
                         "default of a uuid many2one given as upper-case text")

    def test_many2one_domain_with_uuid_text_matches_ids(self):
        line_model = self.env['test_uuid_ids.line']
        self.assertEqual(line_model.search([('doc_id', '=', str(self.doc.id))]), self.line, "many2one '=' uuid text")
        uuid_texts = [str(self.doc.id).upper(), str(self.other_doc.id)]
        self.assertEqual(line_model.search([('doc_id', 'in', uuid_texts)]), self.line, "many2one 'in' uuid texts")

    def test_one2many_domain_with_uuid_text_matches_ids(self):
        self.assertEqual(self.env['test_uuid_ids.doc'].search([('line_ids', '=', str(self.line.id))]), self.doc,
                         "one2many '=' uuid text")

    def test_many2many_domain_with_uuid_text_matches_ids(self):
        self.assertEqual(self.env['test_uuid_ids.line'].search([('tag_ids', '=', str(self.other_doc.id))]), self.line,
                         "many2many '=' uuid text")

    def test_child_of_domain_with_uuid_text_matches_ids(self):
        doc_model = self.env['test_uuid_ids.doc']
        child = doc_model.create({'name': 'Doc A child', 'parent_id': self.doc.id})
        self.assertEqual(doc_model.search([('id', 'child_of', str(self.doc.id))]), self.doc | child,
                         "child_of uuid text returns the record and its children")

    def test_domain_with_name_text_searches_names(self):
        line_model = self.env['test_uuid_ids.line']
        self.assertEqual(line_model.search([('doc_id', '=', 'Doc A')]), self.line, "many2one '=' name text")
        self.assertEqual(line_model.search([('doc_id', 'ilike', 'Doc B')]), line_model,
                         "many2one 'ilike' name with no match")
        self.assertEqual(self.env['test_uuid_ids.doc'].search([('line_ids', '=', 'Line 1')]), self.doc,
                         "one2many '=' name text")
        self.assertEqual(line_model.search([('tag_ids', '=', 'Doc B')]), self.line, "many2many '=' name text")

    def test_unlink_uuid_record_applies_ondelete(self):
        self.ref.doc_id = self.doc
        self.doc.unlink()
        self.assertFalse(self.line.exists(), "ondelete cascade from a uuid model to a uuid model")
        self.assertFalse(self.ref.doc_id, "ondelete set null from an integer model to a uuid model")
        self.assertTrue(self.other_doc.exists(), "unrelated uuid record survives")

    def test_unlink_integer_record_restricted_by_uuid_record(self):
        with self.assertRaises(IntegrityError, msg="ondelete restrict from a uuid model to an integer model"):
            with mute_logger('odoo.sql_db'), self.cr.savepoint():
                self.partner.unlink()

    def _get_column_type(self, table, column):
        self.env.cr.execute("""
            SELECT udt_name, column_default FROM information_schema.columns
             WHERE table_name = %s AND column_name = %s
        """, [table, column])
        return self.env.cr.fetchone()
