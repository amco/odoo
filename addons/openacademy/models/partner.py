from openerp import models


from openerp import fields
from openerp import api

class Partner(models.Model):
  _name = "res.partner"
  _inherit = ["res.partner"]
  instructor = fields.Boolean(string="Instructor")
