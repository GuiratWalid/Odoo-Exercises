# Exercise 4: Add the contact type feature

## Task
Implement an Odoo module to enable the creation of contacts with a specific type (e.g., Prospect, Client, Partner, Supplier, etc.) and allow the management of sub-contacts.

### What to Do:

1. **Creation of a Contact Type Field**
   Create a new field in the res.partner model to specify the contact type. This field should be a selection list with the following options:
    * **Prospect**
    * **Client**
    * **Partner**
    * **Supplier**
    The field must be visible when creating or editing a contact.

2. **Classify Contacts by Type**
   Configure the list view (tree view) so that contacts are automatically sorted by their type. Use a filtering or grouping mechanism in the user interface to organize the contacts by type.

3. **Add the Ability to Create Sub-Contacts**
   Create a relational field (of type many2one or one2many) in the res.partner model to link a contact to a sub-contact. When creating a new contact, it should be possible to select an existing parent contact or directly create a new sub-contact.

4. **Choose a Parent Contact When Creating a New Contact**
    When creating a new contact, allow the user to specify whether it belongs to an existing contact or not. This can be achieved by adding a relational field linked to res.partner.

---

**Good luck and happy coding!**
