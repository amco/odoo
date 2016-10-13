# -*- coding: utf-8 -*- 

from openerp import models
from openerp import fields
from openerp import api

class AmcoStudent(models.Model):
  _name = "ao.student"

  name = fields.Char(string="Student name")
  partner_id = fields.Many2one(comodel_name="res.partner", string="Partner", domain=[("roles", "=", "student")])
  school_id = fields.Many2one(comodel_name="ao.school")
  active = fields.Boolean(string="Active")
  display_name = fields.Char(string="Display Name")
  count = fields.Integer(string="Count", default=1)
