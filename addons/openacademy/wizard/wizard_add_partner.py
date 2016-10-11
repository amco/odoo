from openerp import models
from openerp import fields
from openerp import api
from openerp import exceptions


class WizardAddPartner(models.TransientModel):
  _name = "wizard.add.partner"
  partner_ids = fields.Many2one(comodel_name="res.partner", string="Partner")
  count       = fields.Integer(string="Count")
