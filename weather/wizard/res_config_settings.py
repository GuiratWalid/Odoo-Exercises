from odoo import models, fields


class ResConfigSettings(models.TransientModel):
    _inherit = "res.config.settings"

    #=== Fields ===#

    weather_api_key = fields.Char(
        string="Weather API Key",
        config_parameter="weather.weather_api_key"
    )

    position_stack_api_key = fields.Char(
        string="Position Stack API Key",
        config_parameter="weather.position_stack_api_key"
    )