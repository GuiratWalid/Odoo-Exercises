from odoo import models, fields


class WeatherHourlyForecast(models.Model):
    _name = "weather.hourly.forecast"
    _description = "Weather Hourly Forecasts"

    #=== General Fields ===#

    time = fields.Char(
        string="Time",
        required=True,
        help="Time of the forecast (e.g., 01:00 AM)"
    )
    temperature = fields.Float(
        string="Temperature (°C)",
        help="Temperature at the specified time"
    )
    feels_like = fields.Float(
        string="Feels Like (°C)",
        help="Perceived temperature at the specified time"
    )
    condition = fields.Char(
        string="Condition",
        help="Weather condition (e.g., Clear, Rainy)"
    )
    uv_index = fields.Float(
        string="UV Index",
        help="UV Index at the specified time"
    )

    #=== Daily Forecasts Field ===#

    daily_forecast_id = fields.Many2one(
        "weather.daily.forecast",
        string="Daily Forecast"
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

    #=== Other Weather Details Fields ===#

    humidity = fields.Integer(
        string="Humidity (%)",
        readonly=True
    )
    pressure = fields.Float(
        string="Pressure (mBar)",
        readonly=True
    )
    amount_precipitation = fields.Float(
        string="Amount Precipitation (mm)",
        readonly=True
    )
