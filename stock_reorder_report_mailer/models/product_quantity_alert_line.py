import logging

from odoo import models, fields, api
from odoo.exceptions import ValidationError

# Initialize logger for tracking issues
_logger = logging.getLogger(__name__)


class ProductQuantityAlertLine(models.Model):
    _name = "product.quantity.alert.line"
    _description = "This module allows setting an alert threshold for the quantity of a specific product in a location."

    # Fields
    location_id = fields.Many2one(
        comodel_name="stock.location",
        string="Location",
        domain=[("usage", "=", "internal")],
    )
    alert_qty = fields.Float(string="Alert Quantity", default=0, required=True)
    product_tmpl_id = fields.Many2one(comodel_name="product.template")

    # Constraints
    @api.constrains("alert_qty")
    def _check_alert_qty(self):
        if any(record.alert_qty < 0 for record in self):
            _logger.warning("Alert quantity must be positive for one or more records.")
            raise ValidationError("The alert quantity must be positive.")
