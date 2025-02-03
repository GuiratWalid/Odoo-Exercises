from odoo import models, fields, api, _
from odoo.exceptions import ValidationError


class WeatherAlert(models.Model):
    _name = "weather.alert"
    _description = "Weather Alerts"

    #=== General Fields ===#

    name = fields.Char(
        string="Name",
        required=True,
        copy=False,
        default=lambda self: self.env['ir.sequence'].next_by_code('weather.alert')
    )

    #=== Temperature Fields ===#

    temp_max = fields.Float(
        string="Max Temperature"
    )
    temp_min = fields.Float(
        string="Min Temperature"
    )

    #=== Other Fields ===#

    wind_max = fields.Float(
        string="Max Wind"
    )
    amount_precipitation_max = fields.Float(
        string="Max Amount Precipitation"
    )

    #=== Contraint Methods ===#

    @api.constrains('temp_min', 'temp_max')
    def _check_temperature_range(self):
        """
             Ensures that 'temp_min' is not greater than 'temp_max'.
             Raises a ValidationError if the condition is violated.
        """
        for record in self:
            if record.temp_min and record.temp_max and record.temp_min > record.temp_max:
                raise ValidationError(
                    _("The minimum temperature \"%s°C\" cannot be higher than the maximum temperature \"%s°C\".") %
                    (record.temp_min, record.temp_max)
                )
