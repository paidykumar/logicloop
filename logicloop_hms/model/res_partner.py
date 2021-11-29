
from odoo import api, fields, models, _

class res_partner(models.Model):
    _inherit = 'res.partner'

    is_patient = fields.Boolean(string='Patient')
    is_doctor = fields.Boolean(string="Doctor")

