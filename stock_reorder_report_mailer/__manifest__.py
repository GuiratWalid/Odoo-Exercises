{
    "name": "Stock Reorder Report Mailer",
    "version": "1.0",
    "author": "Walid Guirat",
    "category": "Inventory/Stock",
    "summary": "Automate the low stock alerts",
    "description": """
Inventory
====================
The Stock Alert Report Mailer module for Odoo automates the monitoring of inventory levels for stockable products.
It sends regular email reports to designated users, highlighting products with quantities that have reached or fallen below their predefined minimum alert thresholds.
This proactive reporting helps inventory managers quickly identify low-stock items and take timely actions to replenish inventory, preventing stockouts and ensuring optimal stock levels.
    """,
    "depends": ["product", "stock"],
    "data": [
        "security/ir.model.access.csv",
        "views/product_template_views.xml",
        "views/stock_reorder_report_template.xml",
        "report/stock_reorder_report.xml",
        "data/mail_template_data.xml",
        "data/ir_cron_data.xml",
    ],
    "installable": True,
    "license": "LGPL-3",
}
