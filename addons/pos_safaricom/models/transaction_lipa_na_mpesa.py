from odoo import models, fields


class TransactionLipaNaMpesa(models.Model):
    _name = 'transaction.lipa.na.mpesa'
    _description = 'Transaction Lipa na M-PESA'

    trans_id = fields.Char(string="Transaction ID")
    name = fields.Char()
    amount = fields.Integer()
    number = fields.Char()
    received_at = fields.Datetime()
