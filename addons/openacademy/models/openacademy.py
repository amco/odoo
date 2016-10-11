# -*- coding: utf-8 -*-

import pytz
import dateutil
from dateutil.relativedelta import relativedelta

from datetime import datetime
from openerp import models
from openerp import fields
from openerp import api
from openerp import exceptions
from openerp import _

from openerp.tools import DEFAULT_SERVER_DATETIME_FORMAT

class OpenacademySession(models.Model):
  _name = "openacademy.session"
  _inherit = ["mail.thread"]

  # Fields definition
  name = fields.Char(string="Session Title", size=200, translate=True, required=True, copy=False)
  # name field is the recognizable record field use in views
  code          = fields.Char(string="Code", size=16)
  active        = fields.Boolean(string="Active", default=True, track_visibility="always")
  max_seat      = fields.Integer(string="Maximum Seats", required=True, default=10, index=True, readonly=True, states={"new": [("readonly", False)]})
  duration_days = fields.Float(string="Duration(days)", digits=(6,3), required=True, default=1, readonly=True, states={"new": [("readonly", False)]})
  start_date    = fields.Datetime(string="Start Date", track_visibility="onchange", readonly=True, states={"new": [("readonly", False)]}) # can be always|onchange
  end_date      = fields.Datetime(string="End Date", track_visibility="onchange", readonly=True, states={"new": [("readonly", False)]})
  is_public     = fields.Boolean(string="Is Public Event?",  readonly=True, states={"new": [("readonly", False)]})
  notes         = fields.Text(string="Notes",  readonly=True, states={"new": [("readonly", False)]})
  contain       = fields.Html(string="Session Course",  readonly=True, states={"new": [("readonly", False)]})
  banner        = fields.Binary(string="Banner",  readonly=True, states={"new": [("readonly", False)]})
  state         = fields.Selection(string="State", selection=[("new", "New"), ("approve", "Approve"), ("reject", "Rejected"), ("open", "Open"), ("done", "Done")], default="new")
  instructor_id = fields.Many2one(comodel_name="res.partner", string="Instructor", ondelete="restrict",  readonly=True, states={"new": [("readonly", False)]})
  course_id     = fields.Many2one(comodel_name="openacademy.course", string="Course",  readonly=True, states={"new": [("readonly", False)]})
  tag_ids       = fields.Many2many(comodel_name="openacademy.tag", relation="rel_session_tags", column1="session_id", column2="tag_id", string="Tags")
  attendee_ids  = fields.One2many(comodel_name="openacademy.attendee", inverse_name="session_id", string="Attendees",  readonly=True, states={"new": [("readonly", False)]})

  total_invited = fields.Integer(compute='_compute_total_invited', string="Total Invited")
  total_attending = fields.Integer(compute='_compute_total_invited', string="Total Attending")

  _sql_constraints = [
        ("session_code_unique", "unique (code)", _("The code must be unique !")),
      ]

  @api.multi
  @api.depends("attendee_ids")
  def _compute_total_invited(self):
    for record in self:
      self.total_invited = sum([att.count for att in record.attendee_ids ])
      self.total_attneding = sum([att.count for att in record.attendee_ids if att.state == "going"])

  # :-(
  @api.model
  def create(self, values):
    if not values.get("code"):
      values['code'] = values.get("name")[:16].upper()

    return super(OpenacademySession, self).create(values)

  #Data Validation
  @api.constrains("start_date", "end_date")
  def date_validation(self):
    if self.start_date > self.end_date:
      local = pytz.timezone(self.env.context.get('tz'))

      start_date = datetime.strptime(self.start_date, DEFAULT_SERVER_DATETIME_FORMAT)
      end_date = datetime.strptime(self.end_date, DEFAULT_SERVER_DATETIME_FORMAT)

      local_start = local.localize(start_date, is_dst=None).strftime("%d/%m/%Y")
      local_end = local.localize(end_date, is_dst=None).strftime("%d/%m/%Y")

      msg = _("Session starting on %s, should not be set after end date(%s)" % (local_end, local_start))
      raise exceptions.ValidationError(msg)

  #callback on chnage
  @api.onchange("start_date")
  def onchange_start_date(self):
    if self.start_date:
      date = datetime.strptime(self.start_date, DEFAULT_SERVER_DATETIME_FORMAT)
      self.end_date = date + relativedelta(days=self.duration_days)

  @api.multi
  def action_approve_session(self):
    for record in self:
      record.state = "approve"
