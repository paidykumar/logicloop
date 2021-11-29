
from odoo import models, fields, api, _

class medical_physician(models.Model):
    _name="medical.physician"
    _rec_name = 'partner_id'

    partner_id = fields.Many2one('res.partner','Physician',required=True)
    institution_partner_id = fields.Many2one('res.partner',domain=[('is_institution','=',True)],string='Institution')
    code = fields.Char('Id')
    info = fields.Text('Extra Info')
    medical_appointments_ids = fields.One2many('medical.appointment', 'doctor_id', string='Appointments')
