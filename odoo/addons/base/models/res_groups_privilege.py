from odoo import fields, models


class ResGroupsPrivilege(models.Model):
    _name = 'res.groups.privilege'
    _description = "Privilege"
    _order = 'sequence, name, id'

    name = fields.Char(required=True, translate=True)
    description = fields.Text(translate=True)
    placeholder = fields.Char(string='No group label', default=lambda self: self.env._('No'), translate=True,
        help="Label displayed when the user does not belong of any group of that scope.")
    sequence = fields.Integer(default=100)
    category_id = fields.Many2one('ir.module.category', index=True)
    group_ids = fields.One2many('res.groups', 'privilege_id', string='Groups')
