import logging

import requests

from odoo import models, fields, api, _
from odoo.exceptions import UserError, ValidationError

from datetime import timedelta

_logger = logging.getLogger(__name__)


class GenerateDailyForecastWizard(models.TransientModel):
    _name = 'generate.daily.forecast.wizard'
    _description = "Generate daily weather forecast"

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

    @api.model
    def action_show_alert(self, title, message, type, sticky):
        """Displays a notification to the user."""
        return {
            'type': 'ir.actions.client',
            'tag': 'display_notification',
            'params': {
                'title': title,
                'message': message,
                'type': type,
                'sticky': sticky,
            },
        }

    @api.model
    def action_redirect_daily_forecast(self):
        """Redirects to the list view of daily forecasts."""
        return {
                'name': 'Daily Forecasts',
                'res_model': 'weather.daily.forecast',
                'type': 'ir.actions.act_window',
                'view_mode': 'list',
                'target': 'current'
            }

    #=== Getter methods ===#

    def _get_weather_api_key(self):
        """Fetches Weather API key from system parameters."""
        _logger.info("Fetching the Weather API key from system parameters.")
        key = "weather.weather_api_key"
        weather_api_key =  self.env['ir.config_parameter'].sudo().get_param(key, default=None)

        if not weather_api_key:
            _logger.warning("Weather API key is not set in system parameters.")
            raise UserError(
                _("Weather API Key is not configured. Please set it in the system parameters.")
            ) from None

        _logger.debug(f"Retrieved Weather API key: {weather_api_key}")
        return weather_api_key

    def _get_api_url(self, endpoint):
        """Returns the full API URL for a given endpoint."""
        return f"https://api.weatherapi.com/v1/{endpoint}"

    def _get_wind_max(self, forecast_hours):
        """Returns the maximum wind speed from forecast hours."""
        return max(forecast_hour["wind_mph"] for forecast_hour in forecast_hours)

    def _get_wind_min(self, forecast_hours):
        """Returns the minimum wind speed from forecast hours."""
        return min(forecast_hour["wind_mph"] for forecast_hour in forecast_hours)

    #=== Business Methods ===#

    def _create_daily_forecast(self, api_data):
        """Creates daily and hourly forecast records from API data."""
        self.ensure_one()
        if api_data and api_data["forecast"]:
            for forecast in api_data["forecast"]["forecastday"]:
                date = forecast["date"]
                forecast_exist = self.env['weather.daily.forecast'].search([
                    ('date', '=', date),
                    ('location_id', '=', self.location_id.id),
                ])
                if not forecast_exist:
                    daily_forecast = self.env['weather.daily.forecast'].create({
                        'date': forecast["date"],
                        'location_id': self.location_id.id,
                        'temp_current': forecast["day"]["avgtemp_c"],
                        'temp_max': forecast["day"]["maxtemp_c"],
                        'temp_min': forecast["day"]["mintemp_c"],
                        'wind_current': api_data["current"]["wind_mph"],
                        'wind_degree': api_data["current"]["wind_degree"],
                        'wind_direction': api_data["current"]["wind_dir"],
                        'wind_max': self._get_wind_max(forecast["hour"]),
                        'wind_min': self._get_wind_min(forecast["hour"]),
                        'condition': forecast["day"]["condition"]["text"],
                        'humidity': forecast["day"]["avghumidity"],
                        'uv_index': api_data["current"]["uv"],
                        'pressure': api_data["current"]["pressure_mb"],
                        'sunrise': forecast["astro"]["sunrise"],
                        'sunset': forecast["astro"]["sunset"],
                    })
                    if daily_forecast:
                        for forecast_hour in forecast["hour"]:
                            self.env["weather.hourly.forecast"].create({
                                'time': forecast_hour["time"],
                                'temperature': forecast_hour["temp_c"],
                                'feels_like': forecast_hour["feelslike_c"],
                                'condition': forecast_hour["condition"]["text"],
                                'uv_index': forecast_hour["uv"],
                                'daily_forecast_id': daily_forecast.id,
                                'humidity': forecast_hour["humidity"],
                                'pressure': forecast_hour["pressure_mb"],
                                'wind_current': forecast_hour["wind_mph"],
                                'wind_degree': forecast_hour["wind_degree"],
                                'wind_direction': forecast_hour["wind_dir"],
                                'amount_precipitation': forecast_hour["precip_mm"]
                            })
                    else:
                        _logger.error("Failed to create a daily forecast")
                        raise ValidationError(
                            _("Failed to create a daily forecast. Please try again later.")
                        ) from None
                else:
                    _logger.warning("Trying to create an existing forecast")
                    self.action_show_alert(
                        title=_("Warning"),
                        message=_("The forecast for the {} region on {} already exists.").format(self.location_id.name, date),
                        type="warning",
                        sticky=False
                    )

    def generate_weather_forecast(self):
        """Generates weather forecast by calling Weather API."""
        self.ensure_one()

        api_url = self._get_api_url("forecast.json")

        params = {
            "key": self._get_weather_api_key(),
            "q": self.location_id.city,
            "days": self.days_forecast,
            "dt": self.date_from
        }

        try:
            response = requests.get(api_url, params=params)
            response.raise_for_status()
            response_data = response.json()
            self._create_daily_forecast(response_data)
            return self.action_redirect_daily_forecast()
        except requests.exceptions.RequestException as e:
            _logger.error("Request to Weather API failed: %s", e)
            raise ValidationError(
                _("Failed to generate weather forecast. Please try again later.")
            ) from None
        except ValueError:
            _logger.error("Invalid response from Weather API: %s", response.text)
            raise ValidationError(
                _("Failed to generate weather forecast. Please contact support.")
            ) from None

    #=== Contraint Methods ===#

    @api.constrains('days_forecast', 'date_from')
    def _check_days_forecast(self):
        """Ensures 'days_forecast' is between 1 and 3."""
        for record in self:
            if not (1 <= record.days_forecast <= 3):
                raise ValidationError(
                    _("Days forecast must be between 1 and 3.")
                ) from None
            max_date_from = fields.Date.today() + timedelta(days=14)
            min_date_from = fields.Date.today()
            if not (min_date_from <= record.date_from <= max_date_from):
                raise ValidationError(
                    _("Date from must be between {} and {}.").format(min_date_from, max_date_from)
                ) from None
