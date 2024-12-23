from odoo import models, fields

CONTACT_TYPES = [
    ('prospect', 'Prospect'),
    ('customer', 'Customer'),
    ('partner', 'Partner'),
    ('supplier', 'Supplier'),
]


class ResPartner(models.Model):
    _inherit = "res.partner"

    # === fields ===#

    contact_type = fields.Selection(
        string="Contact Type",
        selection=CONTACT_TYPES,
        help="Specify the type of contact."
    )

    parent_contact_id = fields.Many2one(
        comodel_name='res.partner',
        string='Parent Contact',
        help="The parent contact for this sub-contact."
    )

    sub_contact_ids = fields.One2many(
        comodel_name='res.partner',
        inverse_name='parent_contact_id',
        string='Sub-contacts',
        help="The sub-contacts for this contact."
    )
