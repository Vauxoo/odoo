# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import fields, models


class District(models.Model):
    _name = 'res.district'
    _description = 'District'
    _order = 'name'

    name = fields.Char("District Name", required=True, translate=True)
    city_id = fields.Many2one('res.city', 'City')
    code = fields.Char(
        string='District Code', help='The district code.', required=True)
