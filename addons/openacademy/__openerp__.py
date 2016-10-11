# -*- coding: utf-8 -*-
{
  "name": "Open Academy",
  "version": "1.0",
  "summuary": "Session, Course Management",
  "sequence": "1",
  "description": """
Open Academy Management
===============================
- Course Management
- **Session Management**

""",
  "depends": ["mail"],
  "category": "Tools",
  "data": [
      "security/openacademy_security.xml",
      "security/ir.model.access.csv",
      "wizard/wizard_add_partner_views.xml",
      "views/openacademy_views.xml",
      "views/partner_views.xml",
      "views/openacademy_workflow.xml",
      "views/report_openacademy_session.xml",
      "views/report_openacademy_session_registration.xml",
    ],
  "demo": [],
}
