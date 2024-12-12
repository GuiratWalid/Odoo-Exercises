from odoo import models, fields


class GetWeatherForecast(models.TransientModel):
    _name = 'get.weather.forecast'
    _description = "Get Weather Forecast"

    #=== Fields ===#

    date_from = fields.Date(
        string="Date From",
        required=True,
        default=fields.Date.today()
    )
    days_forecast = fields.Integer(
        string="Days Forecast",
        required=True,
        default=1
    )
    location_id = fields.Many2one(
        "weather.location",
        string="Location",
        required=True
    )

    #=== Action Methods ===#

    def generate_weather_forecast(self):
        print((record for record in self))
