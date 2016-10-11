# -*- coding: utf-8 -*-

from openerp import models
from openerp import fields

class OpenacademyAttendee(models.Model):
  _name = "openacademy.attendee"

  name = fields.Char(string="Attendee Name", required=True)
  partner_id = fields.Many2one(comodel_name="res.partner", string="Partner")
  email = fields.Char(string="Email")
  count = fields.Integer(string="Invited Individual")
  session_id = fields.Many2one(comodel_name="openacademy.session", string="Session")
  state = fields.Selection(string="Status", selection=[("invite", "Invited"), ("going", "Going to Attned"), ("not", "Not Attending"), ("unsure", "Unsure")], default="invite")
