from odoo import fields, models


class Document(models.Model):
    _name = 'test_uuid_ids.doc'
    _description = 'Document with UUID ids'
    _id_type = 'uuid'

    name = fields.Char(required=True)
    parent_id = fields.Many2one('test_uuid_ids.doc')
    line_ids = fields.One2many('test_uuid_ids.line', 'doc_id')
    ref_ids = fields.One2many('test_uuid_ids.ref', 'doc_id')
    legacy_id = fields.Many2one('test_uuid_ids.legacy')


class Reference(models.Model):
    _name = 'test_uuid_ids.ref'
    _description = 'Record with integer ids pointing to a document'

    name = fields.Char(required=True)
    doc_id = fields.Many2one('test_uuid_ids.doc', ondelete='set null')


class Line(models.Model):
    _name = 'test_uuid_ids.line'
    _description = 'Line with UUID ids pointing to UUID and integer models'
    _id_type = 'uuid'

    name = fields.Char(required=True)
    doc_id = fields.Many2one('test_uuid_ids.doc', ondelete='cascade')
    partner_id = fields.Many2one('res.partner', ondelete='restrict')
    tag_ids = fields.Many2many('test_uuid_ids.doc', 'test_uuid_ids_line_doc_rel', 'line_id', 'doc_id')
    ref_ids = fields.Many2many('test_uuid_ids.ref', 'test_uuid_ids_line_ref_rel', 'line_id', 'ref_id')


class Legacy(models.Model):
    _name = 'test_uuid_ids.legacy'
    _description = 'UUID ids declared on a table that already exists'
    _id_type = 'uuid'

    name = fields.Char()
    code = fields.Char()
