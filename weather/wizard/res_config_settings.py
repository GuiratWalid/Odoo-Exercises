from odoo import models, fields ,api


class ResConfigSettings(models.TransientModel):
    _inherit = "res.config.settings"

    #=== Fields ===#

    weather_api_key = fields.Char(
        string="Weather API Key",
        config_parameter="weather.weather_api_key"
    )