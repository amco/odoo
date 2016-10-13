# -*- coding: utf-8 -*-

import re
import datetime
from datetime import datetime
import dateutil
from dateutil.relativedelta import relativedelta

from openerp import models
from openerp import fields
from openerp import api
from openerp import exceptions

from openerp import _

from openerp.tools import DEFAULT_SERVER_DATETIME_FORMAT

class AoSchool(models.Model):
  _name = "ao.school"

  _SCHOOL_TYPES = [
      ("preschool", _("Preschool")),
      ("elementary", _("Elementary")),
      ("middleschool", _("Middle School")),
      ("highschool", _("High School")),
      ]

  _SCHOOL_STATE = [
        ("lead", _("Lead")),
        ("prospect", _("Prospect")),
        ("closed", "Closed"),
        ("qualified", _("Qualified Prospect")),
        ("opportunity", _("Opportunity")),
      ]

  name = fields.Char(string="School Name", size=200, required=True, states={"closed": [("readonly",True)]})
  code = fields.Char(string="Code", size=24, readonly=True, states={"lead": [("readonly", False)]})
  phone = fields.Char(string="Phone", size=11)
  country = fields.Char(string="Country", size=2, default="mx")
  active = fields.Boolean(string="Active", states={"closed": [("readonly", True)]})
  type = fields.Selection(string="Tipo de Colegio", selection=_SCHOOL_TYPES, index=True)
  census = fields.Integer(string="Census", default=1)
  established = fields.Datetime(string="Established on")

  coordinator_id = fields.Many2one(comodel_name="res.partner", domain=[('function', '=', 'Coordinator')])
  student_ids = fields.One2many(comodel_name="ao.student", inverse_name="school_id", string="Student", states={"closed": [("readonly", True)]})

  responsible_id = fields.Many2one(comodel_name="res.users")

  contract = fields.Html(string="Current Contract")
  logo = fields.Binary(string="School Logo")

  state = fields.Selection(string="State", selection=_SCHOOL_STATE, default="lead")

  loyalty_years=fields.Integer(compute="_get_loyalty_years", string="Loyalty")

  count_students = fields.Integer(compute="_get_count_students", string="Total Students")

  _sql_constraints = [
        ("school_code_unique", "unique (code)", "The code must be unique!"),
      ]

  @api.constrains("phone")
  def phone_validation(self):
    valid_phone = re.match(r'\+?\d{3}[- ]?\d{3}[- ]?\d{4}', self.phone)
    if not valid_phone:
      raise exceptions.ValidationError("Please use valid phone.")

  @api.model
  def create(self, values):
    phone = values.get("phone")
    if phone and not re.match(r'^\+', phone):
      values["phone"] = "+%s" % (phone)

    return super(AoSchool, self).create(values)

  @api.multi
  @api.depends("established")
  def _get_loyalty_years(self):
    for record in self:
      if record.established:
        established = datetime.strptime(record.established, DEFAULT_SERVER_DATETIME_FORMAT)
        record.loyalty_years = relativedelta(datetime.now(), established).years

  @api.multi
  @api.depends("student_ids")
  def _get_count_students(self):
    for record in self:
      record.count_students = sum([att.count for att in record.student_ids])

  @api.multi
  def action_qualify(self):
    for record in self:
      if record.count_students > 10:
        record.state = True
        record.state = "prospect"

  @api.multi
  def action_close(self):
    for record in self:
      record.state = "closed"
      record.active = False
