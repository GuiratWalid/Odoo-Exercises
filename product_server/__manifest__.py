{
    "name": "Product Server",
    "version": "1.0",
    "author": "Walid Guirat",
    "category": "Inventory/Product",
    "summary": "Odoo Product Server",
    "description": """
Inventory
====================
This Odoo module implements a REST API to manage product and warehouse data. It provides endpoints to:
1. List all stockable products in the database.
2. Retrieve specific properties of a product by its ID.
3. Calculate and display the total cost of products by location within a specified warehouse, giving a detailed breakdown per location.

Ideal for seamless integration with external systems, this module enables real-time access to essential product and inventory valuation data.
    """,
    "depends": ["base", "product", "stock"],
    "data": [],
    "installable": True,
    "license": "LGPL-3",
}
