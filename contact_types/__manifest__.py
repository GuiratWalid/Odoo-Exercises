{
    "name": "Contact Types",
    "version": "18.0.1.0.0",
    "author": "Walid Guirat",
    "category": "Contacts/Management",
    "summary": "Manage contacts with specific types and sub-contacts",
    "description": """
Contacts Management
====================
The Advanced Contact Manager module for Odoo enhances the default contact management by introducing the ability to categorize contacts into specific types (e.g., Prospect, Client, Partner, Supplier, etc.) and manage sub-contacts effectively.
This module is designed to provide better organization and hierarchy in contact relationships, enabling businesses to streamline their communication and operations.
    """,
    "depends": ["contacts"],
    "data": [
        "views/res_partner.xml"
    ],
    "installable": True,
    "license": "LGPL-3"
}