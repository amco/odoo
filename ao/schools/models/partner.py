from openerp import models
from openerp import fields

class Partner(models.Model):
  _inherit = ["res.partner"]

  _ROLES = [
      ("coordinator", "Coordinator"),
      ("admin", "Administrator"),
      ("supervisor", "Supervisor"),
      ("teacher", "Teacher"),
      ("student", "Student"),
    ]

  roles = fields.Selection(string="Role", selection=_ROLES)
