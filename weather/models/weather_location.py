from odoo import models, fields ,api


class WeatherLocation(models.Model):
    _name = "weather.location"
    _description = "Represents the locations for which weather forecasts are collected."

    #=== Fields ===#

    name = fields.Char(
        string="Location Name",
        compute="_compute_name",
        store=True
    )
    state_id = fields.Many2one(
        "res.country.state",
        string="Region",
        required=True
    )
    country_id = fields.Many2one(
        "res.country",
        string="Country",
        required=True
    )
    latitude = fields.Float(
        string="Latitude",
        digits=(10, 6),
        help="Latitude of the location",
        readonly=True
    )
    longitude = fields.Float(
        string="Longitude",
        digits=(10, 6),
        help="Longitude of the location",
        readonly=True
    )

    #=== Compute Methods ===#

    @api.depends("state_id", "state_id.name", "country_id", "country_id.name")
    def _compute_name(self):
        for record in self:
            record.name = record.state_id.name + ", " + record.country_id.name if record.state_id and record.state_id.name and  record.country_id and record.country_id.name else ""

    #=== Onchange Methods ===#

    @api.onchange("state_id")
    def _onchange_state_id(self):
        for record in self:
            record.country_id = record.state_id.country_id

    #=== SQL Contraints ===#

    _sql_constraints = [
        ('unique_location', 'unique(name)', 'This location is already exists!')
    ]
