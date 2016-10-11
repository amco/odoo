# -*- coding: utf-8 -*-

from openerp import models
from openerp import fields

class AoSchoolCustomer(models.Model):
  _name = "ao.school.customer"
  _inherit = ["res.partner"]

  teachers = fields.Integer(string="Teachers", default=1)
  zone_code = fields.Char(string="Zone")
  payment_schema = fields.Selection(string="Payment Schema", selection=[("parents", "Parent Paid"), ("school", "School Paid")])
  tax_id = fields.Char(string="Tax ID", size=20)
