from datetime import datetime, timedelta

from odoo import models, fields, api


class WeatherDailyForecast(models.Model):
    _name = "weather.daily.forecast"
    _description = "Weather Daily Forecasts"

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

    #=== Address Fields ===#

    location_id = fields.Many2one(
        "weather.location",
        string="Location",
        required=True
    )
    city = fields.Char(
        related="location_id.city"
    )
    state = fields.Char(
        related="location_id.state_id.name"
    )
    country = fields.Char(
        related="location_id.country_id.name"
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
    feels_like = fields.Float(
        string="Feels Like (°C)",
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
    amount_precipitation = fields.Float(
        string="Amount Precipitation (mm)",
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
        """
            Compute the name of the forecast using the date field.
            The format is set to DD/MM/YYYY.
        """
        for record in self:
            record.name = datetime.strftime(fields.Date.from_string(record.date), "%d/%m/%Y") if record.date else ""

    # === Logic Methods ===#

    def send_alert_email(self):
        """
            Send alert emails to users based on weather conditions.
            The method checks the weather forecast for tomorrow and sends emails to users if certain thresholds are exceeded.
        """
        alerts = self.env['weather.alert'].search([])
        tomorrow_date = (datetime.now() + timedelta(days=1)).strftime('%Y-%m-%d')
        tomorrow_forecasts = self.search([
            ('date', '=', tomorrow_date)
        ])
        email_template = self.env.ref(
            "weather.weather_alert_email_template",
            raise_if_not_found=True,
        )
        for forecast in tomorrow_forecasts:
            for alert in alerts:
                if forecast.temp_max > alert.temp_max or forecast.temp_min < alert.temp_min or forecast.wind_max > alert.wind_max or forecast.amount_precipitation > alert.amount_precipitation_max:
                    email_to = ','.join(user_id.email for user_id in forecast.location_id.user_ids if user_id and user_id.email)
                    if email_template:
                        email_template.send_mail(
                            forecast.id,
                            force_send=True,
                            email_values={
                                'email_to': email_to
                            }
                        )
