import logging

from odoo import models, fields, api
from odoo.exceptions import ValidationError

# Initialize logger for tracking issues
_logger = logging.getLogger(__name__)


class StockQuant(models.Model):
    _inherit = "stock.quant"

    # Fields
    alert_qty = fields.Float(
        string="Alert Quantity", compute="_compute_alert_qty", store=True
    )

    # Compute methods
    @api.depends(
        "location_id",
        "product_id",
        "product_id.product_tmpl_id",
        "product_id.product_tmpl_id.product_qty_alert_line_ids",
    )
    def _compute_alert_qty(self):
        """
        Computes the alert quantity for a product at a specific location.
        The alert quantity is fetched from the `product.quantity.alert.line` model.
        If no alert line is found, the default alert quantity is set to 0.
        """
        for record in self:
            alert_line = 0.0
            if (
                record.location_id
                and record.product_id
                and record.product_id.product_tmpl_id
            ):
                alert_line = self.env["product.quantity.alert.line"].search(
                    [
                        ("location_id", "=", record.location_id.id),
                        ("product_tmpl_id", "=", record.product_id.product_tmpl_id.id),
                    ],
                    limit=1,
                )
            record.alert_qty = alert_line.alert_qty if alert_line else 0.0
            _logger.info(
                "Computed alert quantity for product %s at location %s: %s",
                record.product_id.name,
                record.location_id.name,
                record.alert_qty,
            )

    # Methods
    @api.model
    def _get_low_stock_data(self):
        """
        Retrieves all stock quant records in internal locations where the available quantity
        is less than the alert quantity.
        Returns a filtered recordset of stock quants.
        """
        records_internal_stock_locations = self.env["stock.quant"].search(
            [("location_id.usage", "=", "internal")]
        )
        low_stock_data = records_internal_stock_locations.filtered(
            lambda record: record.quantity - record.alert_qty < 0
        )
        _logger.info(
            "Found %d low stock records that require reorder.", len(low_stock_data)
        )
        return low_stock_data

    @api.model
    def _send_stock_reorder_report(self):
        """
        Sends an email with the stock reorder report. The report is sent using the email template
        defined in the system. If the template is not found, an exception is raised.
        """
        try:
            email_template = self.env.ref(
                "stock_reorder_report_mailer.email_template_stock_reorder_report",
                raise_if_not_found=True,
            )
            if email_template:
                email_template.send_mail(self.id, force_send=True)
                _logger.info(
                    "Stock reorder report email sent for stock quant ID: %d", self.id
                )
        except Exception as e:
            _logger.error(
                "Error sending stock reorder report email for stock quant ID: %d. Error: %s",
                self.id,
                str(e),
            )
            raise ValidationError(
                f"An error occurred while sending the stock reorder report email for stock quant ID {self.id}. "
                f"Error: {str(e)}"
            )
