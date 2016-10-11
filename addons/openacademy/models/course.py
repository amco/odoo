# -*- coding: utf-8 -*-

from openerp import models
from openerp import fields
from openerp import api

class OpenacademyCourse(models.Model):
  """Open Academy Course"""
  _name = "openacademy.course"

  name           = fields.Char(string="Course Name", required=True)
  code           = fields.Char(string="Code")
  responsible_id = fields.Many2one(comodel_name="res.users", string="Responsbile")
  active         = fields.Boolean(string="Active", default=True)
  notes          = fields.Html(string="Notes")
  session_ids    = fields.One2many(comodel_name="openacademy.session", inverse_name="course_id")
  session_count  = fields.Integer(compute="_compute_session_count", string="Session Count")

  @api.multi
  @api.depends("session_ids")
  def _compute_session_count(self):
    for record in self:
      record.session_count = len(record.session_ids)

  @api.multi
  def name_get(self):
    values = []
    for record in self:
      values.append((record.id, "[{}] {}".format(record.code, record.name)))
    return values

  @api.multi
  def open_sessions(self):
    session_action = self.env.ref("openacademy.action_views_openacademy_sessions")
    session_tree_id = self.env.ref("openacademy.view_openacademy_sessions_tree")
    session_form_id = self.env.ref("openacademy.view_openacademy_sessions_form")

    return {
          "name": "Course Session",
          "help": "Get session",
          "type": session_action.type,
          "views": [[session_tree_id, "tree"], [session_form_id, "form"]],
          "target": session_action.target,
          "res_model": session_action.res_model,
          "domain": [("course_id", "=", self[0].id)],
        }
