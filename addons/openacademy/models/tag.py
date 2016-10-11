# -*- coding: utf-8 -*-

from openerp import models
from openerp import fields

class OpenacademyTag(models.Model):
  _name = "openacademy.tag"
  name = fields.Char(string="Name")
  active = fields.Boolean(string="Active", default=True)
