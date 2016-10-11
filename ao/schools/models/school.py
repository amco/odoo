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
        ("qualified", _("Qualified Prospect")),
        ("opportunity", _("Opportunity")),
      ]

  name = fields.Char(string="School Name", size=200, required=True)
  code = fields.Char(string="Code", size=24, readonly=True, states={"lead": [("readonly", False)]})
  phone = fields.Char(string="Phone", size=11)
  country = fields.Char(string="Country", size=2, default="mx")
  active = fields.Boolean(string="Active", default=True)
  type = fields.Selection(string="Tipo de Colegio", selection=_SCHOOL_TYPES, index=True)
  census = fields.Integer(string="Census", default=1)
  established = fields.Datetime(string="Established on")

  coordinator_id = fields.Many2one(comodel_name="res.partner", ondelete="restrict", domain=[('function', '=', 'Coordinator')])
  customer_id = fields.Many2one(comodel_name="ao.school.customer")

  student_ids = fields.One2many(comodel_name="amco.student", string="Student")

  contract = fields.Html(string="Current Contract")
  logo = fields.Binary(string="School Logo")

  state = fields.Selection(string="State", selection=_SCHOOL_STATE, default="lead")

  loyalty_years=fields.Integer(compute="_get_loyalty_years", string="Loyalty")

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
