import logging

import requests

from odoo import models, fields, api, _
from odoo.exceptions import UserError, ValidationError

_logger = logging.getLogger(__name__)


class WeatherLocation(models.Model):
    _name = "weather.location"
    _description = "Weather Locations"

    #=== General Fields ===#

    name = fields.Char(
        string="Location Name",
        compute="_compute_name",
        store=True
    )
    city = fields.Char(
        string="City",
        required=True
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

    #=== List of Users Field ===#

    user_ids = fields.Many2many(
        comodel_name="res.users",
        string="Users",
        help="List of users to receive alert emails"
    )

    #=== Compute Methods ===#

    @api.depends("city", "state_id", "state_id.name", "country_id", "country_id.name")
    def _compute_name(self):
        """ Compute the full location name using city, state and country. """
        for location in self:
            if location.city and location.state_id and location.state_id.name and location.country_id and location.country_id.name:
                location.name = f"{location.city}, {location.state_id.name}, {location.country_id.name}"
            else:
                location.name = ""

    # #=== Onchange Methods ===#

    @api.onchange("state_id")
    def _onchange_state_id(self):
        """ Automatically update the country field when the state changes. """
        for location in self:
            if location.state_id and location.state_id.country_id:
                location.country_id = location.state_id.country_id

    #=== Getter Methods ===#

    def get_location(self):
        """ Get the location in a queryable format, prioritizing coordinates. """
        self.ensure_one()
        if self.latitude and self.longitude:
            return f"{self.latitude},{self.longitude}"
        elif self.city:
            return self.city
        elif self.state_id:
            return self.state_id.name
        else:
            return self.country_id.name

    def _get_position_stack_api_key(self):
        """ Retrieve the Position Stack API key from system parameters. """
        _logger.info("Fetching the Position Stack API key from system parameters.")
        key = "weather.position_stack_api_key"
        position_stack_api_key = self.env['ir.config_parameter'].sudo().get_param(key, default=None)
        if not position_stack_api_key:
            _logger.warning("Position Stack API key is not set in system parameters.")
            raise UserError("Position Stack API Key is not configured. Please set it in the system parameters.")

        _logger.debug(f"Retrieved Position Stack API key: {position_stack_api_key}")
        return position_stack_api_key

    def _get_position_stack_api_url(self, endpoint):
        """ Build the full API URL for Position Stack. """
        return f"https://api.positionstack.com/v1/{endpoint}"

    def _get_coordinates(self, api_data):
        """ Extract latitude and longitude from the API response. """
        self.ensure_one()
        print(api_data)
        if api_data and api_data["data"]:
            for location in api_data["data"]:
                if location["country"] == self.country_id.name:
                    return location["latitude"], location["longitude"]
        _logger.warning("Location not found! Please verify the location.")
        raise ValidationError(
            _("Location not found! Please verify the location.")
        ) from None

    #=== Logic Methods ===#

    def _fetch_coordinates(self):
        """ Fetch coordinates from the Position Stack API. """
        self.ensure_one()
        api_url = self._get_position_stack_api_url("forward")

        params = {
            "access_key": self._get_position_stack_api_key(),
            "query": self.get_location()
        }

        try:
            response = requests.get(api_url, params=params)
            response.raise_for_status()
            response_data = response.json()
            return self._get_coordinates(response_data)
        except requests.exceptions.RequestException as e:
            _logger.error("Request to Position Stack API failed: %s", e)
            raise ValidationError(
                _("Unable to retrieve location coordinates. Please contact support for assistance.")
            ) from None
        except ValueError:
            _logger.error("Invalid response from Position Stack API: %s", response)
            raise ValidationError(
                _("Unable to retrieve location coordinates. Please contact support for assistance.")
            ) from None

    #=== Action Methods ===#

    def get_coordinates(self):
        """ Public method to fetch coordinates for locations. """
        print(self)
        for location in self:
            latitude, longitude = location._fetch_coordinates()
            location.write({
                'latitude': latitude,
                'longitude': longitude,
            })

    #=== SQL Contraints ===#

    _sql_constraints = [
        ('unique_location', 'unique(name)', 'This location is already exists!')
    ]
