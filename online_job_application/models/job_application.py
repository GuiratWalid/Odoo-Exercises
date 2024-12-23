import time
import random

from odoo import models, fields, api, _

STATE = [
    ("received", "Received"),
    ("in_review", "In Review"),
    ("interview", "Interview"),
    ("accepted", "Accepted"),
    ("rejected", "Rejected")
]


class JobApplication(models.Model):
    _name = "job.application"
    _description = "Job application management module"
    _order = "application_date desc"

    # === General Fields ===#

    name = fields.Char(
        string="Full Name",
        required=True
    )
    job_position_id = fields.Many2one(
        comodel_name="job.position",
        string="Job",
        required=True
    )
    email = fields.Char(
        string="Email",
        required=True
    )
    phone = fields.Char(
        string="Phone"
    )
    resume = fields.Binary(
        string="Resume"
    )
    resume_filename = fields.Char(
        string="Resume Filename"
    )
    cover_letter = fields.Text(
        string="Cover Name"
    )
    state = fields.Selection(
        selection=STATE,
        string="Status",
        default="received",
        required=True
    )

    # === Auto-filled Fields ===#

    application_date = fields.Datetime(
        string="Application Date",
        readonly=True,
        default=fields.Datetime.now
    )
    reference = fields.Char(
        string="Reference",
        readonly=True
    )

    # === CRUD Methods ===#

    @api.model
    def create(self, vals):
        """
            Overriding the create method to auto-generate a unique reference
            for the job application.
        """
        timestamp = int(time.time())
        random_number = random.randint(1000, 9999)
        vals["reference"] = f"CAND-{timestamp}-{random_number}"
        return super(JobApplication, self).create(vals)

    # === Action Methods ===#

    def _send_application_status_update(self):
        """
            Sends an email notification to the candidate about the status update.
        """
        email_template = self.env.ref(
            "online_job_application.email_template_application_status",
            raise_if_not_found=True,
        )
        if email_template:
            email_template.send_mail(self.id, force_send=True)

    def review_action(self):
        """
            Changes the application state to 'In Review' and sends a notification.
        """
        self.ensure_one()
        self.state = "in_review"
        self._send_application_status_update()

    def interview_action(self):
        """
            Changes the application state to 'Interview' and sends a notification.
        """
        self.ensure_one()
        self.state = "interview"
        self._send_application_status_update()

    def accept_action(self):
        """
            Changes the application state to 'Accepted' and sends a notification.
        """
        self.ensure_one()
        self.state = "accepted"
        self._send_application_status_update()

    def reject_action(self):
        """
            Changes the application state to 'Rejected' and sends a notification.
        """
        self.ensure_one()
        self.state = "rejected"
        self._send_application_status_update()

    # === SQL Constraints

    _sql_constraints = [
        ("unique_application", "unique(job_position_id, email)", _("You have already applied for this position."))
    ]
