from odoo import models, fields, api


class JobPosition(models.Model):
    _name = "job.position"
    _description = "Job Position"

    #=== Fields ===#

    name = fields.Char(
        string="Position Name",
        required=True
    )
    description = fields.Text(
        string="Description"
    )
    location = fields.Char(
        string="Location"
    )
    is_published = fields.Boolean(
        string="Published on Website",
        default=False,
        help="Whether the job position is visible on the website or not."
    )
    application_ids = fields.One2many(
        comodel_name="job.application",
        inverse_name="job_position_id",
        string="Applications",
        readonly=True
    )

    #=== Action Methods ===#

    def action_toggle_is_published(self):
        """
            Toggles the publication status of the job position.
            If published, it will become unpublished and vice versa.
        """
        self.ensure_one()
        self.is_published = not self.is_published
