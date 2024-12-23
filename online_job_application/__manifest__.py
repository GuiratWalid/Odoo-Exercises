{
    "name": "Online Job Application",
    "version": "18.0.1.0.0",
    "author": "Walid Guirat",
    "category": "Website",
    "summary": "Module for candidates to apply online",
    "description": """
Online Job Application Module
=============================
Online Job Application Module
=============================
This module allows candidates to apply online for job opportunities via a user-friendly web form.

Key features include:

- A public webpage for candidates to submit their applications.
- Storage of applicant data, including name, email, phone, and uploaded resumes.
- Backend management interface for recruiters to view and manage applications.
- Dashboard for recruiters to track recruitment metrics, including:
  - Total job positions (published/unpublished).
  - Total candidates applied.
  - Application statuses (received, in review, interview, accepted, rejected).
  - Detailed job position statistics.
- Seamless integration with the Odoo website module.

Enhance your recruitment process with this easy-to-use and efficient solution.
   """,
    "depends": ["website"],
    "data": [
        "security/ir.model.access.csv",

        "views/job_position_templates.xml",
        "views/job_application_templates.xml",
        "views/job_position_views.xml",
        "views/job_application_views.xml",
        "views/dashboard_views.xml",
        "views/job_application_menus.xml",

        "data/website_data.xml",
        "data/mail_template_data.xml",
    ],
    'assets': {
        'web.assets_backend': [
            'online_job_application/static/src/js/dashboard.js',
            'online_job_application/static/src/xml/dashboard.xml',
        ],
    },
    "installable": True,
    "license": "LGPL-3"
}
