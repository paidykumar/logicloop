from odoo import api, fields, models, _
from odoo.exceptions import ValidationError
import requests
import logging
import json


class medical_patient(models.Model):
    _name = 'medical.patient'
    _rec_name = 'patient_id'

    @api.onchange('patient_id')
    def _onchange_patient(self):
        address_id = self.patient_id
        self.partner_address_id = address_id

    patient_id = fields.Many2one('res.partner', domain=[('is_patient', '=', True)], string="Patient", required=True)
    name = fields.Char(string='ID', readonly=True)
    extra_info = fields.Char(string='Extra Info')
    last_name = fields.Char('Last Name')
    date_of_birth = fields.Date(string="Date of Birth")
    sex = fields.Selection([('m', 'Male'), ('f', 'Female')], string="Sex")
    mobile = fields.Char("mobile")
    photo = fields.Binary(string="Picture")

    marital_status = fields.Selection(
        [('s', 'Single'), ('m', 'Married'), ('w', 'Widowed'), ('d', 'Divorced'), ('x', 'Separated')],
        string='Marital Status')

    partner_address_id = fields.Many2one('res.partner', string="Address")
    primary_care_physician_id = fields.Many2one('medical.physician', 'Primary Doctor')

    medical_appointments_ids = fields.One2many('medical.appointment', 'patient_id', string='Appointments')

    @api.model
    def create(self, val):
        appointment = self._context.get('appointment_id')
        res_partner_obj = self.env['res.partner']
        if appointment:
            val_1 = {'name': self.env['res.partner'].browse(val['patient_id']).name}
            patient = res_partner_obj.create(val_1)
            val.update({'patient_id': patient.id})

        result = super(medical_patient, self).create(val)
        return result

    @api.constrains("mobile")
    def check_mobile_no(self):
        access_key = "740609c0c770703d7fd0b2bc8f4324af"
        if self.mobile:
            resp = requests.post(
                'http://apilayer.net/api/validate?access_key=' + access_key + '&number=' + self.mobile + '&country_code=IN')
            resp = json.loads(resp.text)
            if resp['valid'] == False:
                raise ValidationError(_("Phone Number is Invalid"))

