import logging

from odoo.tools import column_exists

_logger = logging.getLogger(__name__)


def pre_init_hook(cr):
    pre_create_purchase_method(cr)


def pre_create_purchase_method(cr):
    """Create the purchase_method field in product.template if it does not exist (added in "purchase" dependency).
    Also, set the default value to 'purchase' for existing products by query instead of computing it with Python.
    """
    if not column_exists(cr, "product_template", "purchase_method"):
        cr.execute("ALTER TABLE product_template ADD COLUMN purchase_method character varying;")
        _logger.info("Column 'purchase_method' added to product_template table.")
        cr.execute("UPDATE product_template AS pt SET purchase_method = 'purchase';")
        _logger.info("Setting purchase_method to 'purchase' for %s products", cr.rowcount)
