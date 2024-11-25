from odoo import models, fields


class ProductTemplate(models.Model):
    _inherit = "product.template"

    # Fields
    product_qty_alert_line_ids = fields.One2many(
        comodel_name="product.quantity.alert.line",
        inverse_name="product_tmpl_id",
        string="Alert Quantity Lines",
        help="List of alert quantity lines for each product template",
    )
