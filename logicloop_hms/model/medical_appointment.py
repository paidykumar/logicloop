from odoo import api, fields, models, _
from odoo.exceptions import UserError
from odoo.exceptions import ValidationError


class medical_appointment(models.Model):
    _name = "medical.appointment"
    _inherit = 'mail.thread'

    name = fields.Char(string="Appointment ID", readonly=True, copy=True)

    patient_id = fields.Many2one('medical.patient', 'Patient', required=True)

    appointment_date = fields.Datetime('Appointment Date', required=True, default=fields.Datetime.now)
    appointment_end = fields.Datetime('Appointment End', required=True)
    doctor_id = fields.Many2one('medical.physician', 'Physician', required=True)

    comments = fields.Text(string="Info")
    state = fields.Selection([('draft', 'Draft'), ('accept', 'Accepted'), ('reject', 'Rejected'), ('done', 'Done')],
                             string="State", default='draft')
    reject_reason = fields.Text("Reject Reason")

    # @api.constrains("appointment_date","appointment_end")
    # def check_appointment_date(self):
    #     if self.appointment_date:
    #         pass

    @api.model
    def create(self, vals):
        vals['name'] = self.env['ir.sequence'].next_by_code('medical.appointment') or 'APT'
        msg_body = 'Appointment created'
        for msg in self:
            msg.message_post(body=msg_body)
        result = super(medical_appointment, self).create(vals)
        return result

    def action_accept(self):
        if self.state:
            return {
                'name': ('Accept Date'),
                "type": "ir.actions.act_window",
                "res_model": "mail.message",
                "views": [
                    (self.env.ref('logicloop_hms.view_appoint_for_state_changes').id, 'form')],
                "context": {"default_res_id": self.id, "default_appointment_date": self.appointment_date,
                            "default_appointment_end": self.appointment_end, "to_state": "accept"},
                "target": "new"
            }

    def action_done(self):
        self.write({'state': 'done'})

    def action_reject(self):
        if self.state:
            return {
                'name': ('Accept Date'),
                "type": "ir.actions.act_window",
                "res_model": "mail.message",
                "views": [
                    (self.env.ref('logicloop_hms.view_appoint_for_state_reject').id, 'form')],
                "context": {"default_res_id": self.id, "to_state": "reject"},
                "target": "new"
            }


class MailMessage(models.Model):
    _inherit = "mail.message"

    appointment_date = fields.Datetime('Appointment Date')
    appointment_end = fields.Datetime('Appointment End')
    reject_reason = fields.Text("Reject Reason")

    def add_notes(self):
        obj = self.env['medical.appointment'].sudo().search([('id', '=', self.res_id)])
        appointment_objs = self.env['medical.appointment'].sudo().search(
            [('doctor_id.partner_id', '=', self.env.user.partner_id.id),
             ('id', '!=', self.res_id)])  # self.env.user.partner_id.id
        import logging
        logging.info(appointment_objs)
        for appointment in appointment_objs:
            logging.info(appointment.appointment_end.date())
            logging.info( self.appointment_date.date())
            if self.appointment_date.date() == appointment.appointment_end.date():
                time = self.appointment_date - appointment.appointment_end
                total_seconds = time.total_seconds()
                minutes = total_seconds / 60
                logging.info("total minutes %s" % minutes)
                if abs(minutes) < 15:
                    raise ValidationError(_("please set date 15 minutes before & after the proposed appointment time"))

            if self.appointment_end.date() == appointment.appointment_date.date():
                time = self.appointment_end - appointment.appointment_date
                total_seconds = time.total_seconds()
                minutes = total_seconds / 60
                if abs(minutes) < 15:
                    raise ValidationError(_("please set date 15 minutes before & after the proposed appointment time"))
                logging.info("total minutes %s" % minutes)
        if obj:
            obj.write({"state": self.env.context.get('to_state'),
                       "appointment_date": self.appointment_date,
                       "appointment_end": self.appointment_end})
            return True

    def add_reject_reason(self):
        obj = self.env['medical.appointment'].sudo().search([('id', '=', self.res_id)])
        if obj:
            obj.write({"state": self.env.context.get('to_state'),
                       "reject_reason": self.reject_reason})
            return True
