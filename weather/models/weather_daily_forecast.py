from odoo import models, fields, api

from datetime import datetime


class WeatherDailyForecast(models.Model):
    _name = "weather.daily.forecast"
    _description = "Stores daily weather forecasts."

    #=== General Fields ===#

    name = fields.Char(
        string="Name",
        compute="_compute_name",
        store=True
    )
    date = fields.Date(
        string="Date",
        required=True
    )
    location_id = fields.Many2one(
        "weather.location",
        string="Location",
        required=True
    )

    #=== Temperature Fields ===#

    temp_current = fields.Float(
        string="Current Temperature (°C)",
        readonly=True
    )
    temp_max = fields.Float(
        string="High Temperature (°C)",
        readonly=True
    )
    temp_min = fields.Float(
        string="Low Temperature (°C)",
        readonly=True
    )

    #=== Wind Fields ===#

    wind_current = fields.Float(
        string="Wind (km/h)",
        readonly=True
    )
    wind_degree = fields.Float(
        string="Wind Degree",
        readonly=True
    )
    wind_direction = fields.Char(
        string="Wind Direction",
        readonly=True
    )
    wind_max = fields.Float(
        string="High Wind (km/h)",
        readonly=True
    )
    wind_min = fields.Float(
        string="Low Wind (km/h)",
        readonly=True
    )

    #=== Other Weather Details Fields ===#

    condition = fields.Char(
        string="Condition",
        help="Weather condition, e.g., Clear, Rainy",
        readonly=True
    )
    humidity = fields.Integer(
        string="Humidity (%)",
        readonly=True
    )
    uv_index = fields.Float(
        string="UV Index",
        readonly=True
    )
    pressure = fields.Float(
        string="Pressure (mBar)",
        readonly=True
    )
    sunrise = fields.Char(
        string="Sunrise Time",
        help="Time of sunrise, e.g., 06:30 AM",
        readonly=True
    )
    sunset = fields.Char(
        string="Sunset Time",
        help="Time of sunset, e.g., 06:30 PM",
        readonly=True
    )

    #=== Hourly Forecasts Field ===#

    hourly_forecast_ids = fields.One2many(
        "weather.hourly.forecast",
        "daily_forecast_id",
        string="Hourly Forecasts",
        readonly=True
    )

    #=== Compute Methods ===#

    @api.depends("date")
    def _compute_name(self):
        for record in self:
            record.name = datetime.strftime(fields.Date.from_string(record.date), "%d/%m/%Y") if record.date else ""
