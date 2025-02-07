from odoo import models, fields

class Client(models.Model):
    _inherit = 'res.partner'

    social_object = fields.Text(string='Social Object', help='For businesses only')