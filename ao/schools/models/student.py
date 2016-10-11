# -*- coding: utf-8 -*- 

from openerp import models
from openerp import fields
from openerp import api

class AmcoStudent(models.Model):
  _name = "amco.student"

  name = fields.Char(string="Student name")
  partner_id = fields.Many2one(comodel_name="res.partner", string="Partner")
  school_id = fields.Many2one("ao.school")
  active = fields.Boolean(string="Active")
  display_name = fields.Char(string="Display Name")
