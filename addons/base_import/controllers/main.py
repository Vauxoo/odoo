# Part of Odoo. See LICENSE file for full copyright and licensing details.

import json

from odoo import http
from odoo.http import request
from odoo.tools import BinaryBytes


class ImportController(http.Controller):

    # ruff: disable[builtin-variable-shadowing, builtin-argument-shadowing, builtin-import-shadowing]
    @http.route('/base_import/set_file', methods=['POST'])
    def set_file(self, id, ufile, model=None):
        file = ufile
        written = request.env['base_import.import'].browse(int(id)).write({
            'file': BinaryBytes(file.read()),
            'file_name': file.filename,
            'file_type': file.content_type,
        })

        return json.dumps({'result': written})
    # ruff: enable[builtin-variable-shadowing, builtin-argument-shadowing, builtin-import-shadowing]
