import logging

from odoo import http
from odoo.http import request


_logger = logging.getLogger(__name__)


class WarehouseController(http.Controller):
    @http.route(
        "/api/wh_valuation/<int:wh_id>", type="json", auth="user", methods=["GET"]
    )
    def get_warehouse_valuation(self, wh_id):
        _logger.info(f"GET request received at /api/wh_valuation/{wh_id}")
        try:
            warehouse = request.env["stock.warehouse"].sudo().browse(wh_id)
            if not warehouse.exists():
                _logger.warning(f"Warehouse with ID {wh_id} not found")
                return {"status": 404, "response": {}, "message": "Warehouse not found"}

            locations = request.env["stock.location"].search(
                [("location_id", "child_of", warehouse.view_location_id.id)]
            )
            total_cost = 0
            locations_data = []

            for location in locations:
                quant_total = sum(
                    quant.product_id.standard_price * quant.quantity
                    for quant in location.quant_ids
                )
                total_cost += quant_total
                locations_data.append(
                    {
                        "name": location.name,
                        "total_cost_products": f"{quant_total:.2f} {location.company_id.currency_id.name}",
                    }
                )

            warehouse_data = {
                "id": warehouse.id,
                "name WH": warehouse.name,
                "total_cost": f"{total_cost:.2f} euro",
                "locations": locations_data,
            }
            _logger.info(
                f"Returning valuation for warehouse ID {wh_id} with total cost {total_cost:.2f} {location.company_id.currency_id.name}"
            )
            return {"status": 200, "response": warehouse_data, "message": "Success"}

        except Exception as e:
            _logger.error(f"Error in /api/wh_valuation/{wh_id}: {e}")
            return {"status": 500, "response": {}, "message": str(e)}
