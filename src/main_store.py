from pprint import pprint
from classes.class_Database import (
    IndivEntity,
    LegalEntity,
    Item,
    PurchaseOrder,
    Database,
    Entity,
)
from ui_prompts import confirm, get_po_number
from global_data import VALID_ENTITIES, VALID_ITEMS_IDS_NAMES
from visualization import show_table
from data_formatting import get_invoice_data, get_po_item_qdata
from pdf_creator import create_pdf
from email_service import send_email
from typing import List, Optional, Tuple, Union, Dict
import sys


# Define types for better clarity and checking
Db = Dict[int, Union[Item, Entity, PurchaseOrder, None]]
DbInstance = Union[Item, Entity, PurchaseOrder]

# Global variables will be initialized in database_initialization
items: Optional[Database] = None
entities: Optional[Database] = None
purchase_orders: Optional[Database] = None

# --- Initialization and Debug ---


def database_initialization() -> object:
    """Initializes and loads all databases."""
    global items
    items = Database(initial_db_type="Item")
    pprint("loading data")
    items.load_db()

    global entities
    entities = Database(initial_db_type="Entity")
    entities.load_db()

    global purchase_orders
    purchase_orders = Database(initial_db_type="PurchaseOrder")
    purchase_orders.load_db()

    # fulling the lists with valid entities and items
    update_valid_lists()


def database_debug() -> None:
    """Debug"""
    if entities is None or items is None or purchase_orders is None:
        print("Error: Databases not initialized.")
        return
    pprint(items.db)
    print(type(items.db[1]))
    pprint(entities.db)
    print(VALID_ENTITIES)
    print(VALID_ITEMS_IDS_NAMES)
    pprint(purchase_orders.db)
    print("End of debug output")


def update_valid_lists():
    """Fills global lists with valid entity and item names/IDs."""
    if entities is None or items is None or purchase_orders is None:
        print("Error: Databases not initialized.")
        return

    for entity in entities.db.values():
        if entity is not None:
            if isinstance(entity, IndivEntity):
                VALID_ENTITIES.update({entity._entity_id: entity.last_name})
            elif isinstance(entity, LegalEntity):
                VALID_ENTITIES.update({entity._entity_id: entity.company_name})
            # Skipping the else block, assuming all entities in the DB are typed

    for item in items.db.values():
        if item is not None and isinstance(item, Item):
            VALID_ITEMS_IDS_NAMES.update({item._item_id: item.item_name})


# --- Database Operations ---


def add_i_to_db(db: Database) -> None:
    """Adds item to database and saves it."""
    try:
        # db.add_to_db() returns None on user interrupt
        if db.add_to_db() is None:
            return
    except Exception as e:
        print(f"Exception {e} occurred.")
    db.store_db()


def create_invoice(po_id: int) -> None:
    """Creates an invoice for a given PO ID and handles exceptions."""
    if purchase_orders is None:
        print("Purchase Orders database not initialized.")
        return

    db_item = purchase_orders.db.get(po_id)
    po_instance: Optional[PurchaseOrder] = None

    if isinstance(db_item, PurchaseOrder):
        po_instance = db_item

    if po_instance is None:
        print(f"\nPO ID {po_id} not in database.\n")
        return

    invoice_id = po_id  # Using PO ID as Invoice ID

    try:
        # Check if the object has the create_invoice method (it should be PurchaseOrder)
        if hasattr(po_instance, "create_invoice"):
            po_instance.create_invoice(invoice_id)
            purchase_orders.store_db()
        else:
            print(
                f"Error: Database item for PO ID {po_id} is not a PurchaseOrder instance."
            )
            return

    except Exception:  # Catches the Exception raised by po_instance.create_invoice if invoice already exists
        print("Send invoice anyway?")

        if confirm():
            print("sending")
            send_invoice(po_id)  # Send existing invoice
            return
        else:
            return

    # Send the newly created/updated invoice
    send_invoice(po_id)


def send_invoice(po_id: int) -> None:
    """Generates PDF and sends the invoice via email."""
    if purchase_orders is None or items is None or entities is None:
        print("Required databases not initialized.")
        return

    po_instance: Optional[PurchaseOrder] = None

    if isinstance(db_item := purchase_orders.db.get(po_id), PurchaseOrder):
        po_instance = db_item

    if po_instance is None:
        print(f"Cannot send invoice: PO ID {po_id} not found.")
        return

    file_name = f"Invoice {po_id:06d}"

    # Ensure all required data for get_invoice_data is available
    data = get_invoice_data(po_instance, items, entities)

    create_pdf(data, file_name)

    # Get customer details (safe access required)
    item = entities.db.get(po_instance.customer_id)
    customer: Optional[Entity] = None

    if isinstance(item, Entity) and item is not None:
        customer = item

    # customer = entities.db.get(po_instance.customer_id)
    if customer is None or not hasattr(customer, "email"):
        print(f"Customer ID {po_instance.customer_id} not found or missing email.")
        return

    to_mail = customer.email
    subject = f"Invoice no. {data.get('invoice_id', 'N/A')}"
    attachment_path = f"src/PDF_invoice/{file_name}.pdf"

    try:
        send_email(
            to_email=to_mail,
            subject=subject,
            filename=f"{file_name}.pdf",
            attachment_path=attachment_path,
            body="Dear customer,\n\nPlease find the invoice to your Purchase order in the attachment.\n\nBest regards,",
        )
    except Exception as e:
        print(f"Exception {e} occurred during email sending.")


# ui functions


def op_entities():
    if entities:
        entities.add_to_db()
        entities.store_db()
        update_valid_lists()


def op_items():
    if items:
        items.add_to_db()
        items.store_db()
        update_valid_lists()


def op_purchase_orders():
    if purchase_orders:
        purchase_orders.add_to_db()
        purchase_orders.store_db()


def op_create_invoice():
    if purchase_orders is None:
        print("Purchase Orders database not initialized.")
        return

    print("Choose PO number from the list:")
    show_all_db_i(purchase_orders.db)

    try:
        po_id = get_po_number()
    except Exception:
        print("Invalid input for PO number.")
        return

    if po_id in purchase_orders.db:
        create_invoice(po_id)
    else:
        print("\nPO number not in database.\n")


def op_show_entities():
    if entities:
        show_all_db_i(entities.db)


def op_show_items():
    if items:
        show_all_db_i(items.db)


def op_show_purchase_orders():
    if purchase_orders:
        show_all_db_i(purchase_orders.db)


def show_all_db_i(db) -> None:
    """Shows all database item's values as a table,
    db example: purchase_orders.db"""

    lines: List[Tuple] = []

    if not db:
        print("Database is empty.")
        return

    # Get the header from the first non-None item found
    first_item = next(iter(filter(lambda x: x is not None, db.values())), None)

    if first_item is None:
        print("Database contains no valid items.")
        return

    header: Tuple[str, ...] = first_item.get_header()[0]

    for i in db.keys():
        line = db[i].get_i_data(entities)
        lines += line

    show_table(header, lines, "Show all db items")


def op_show_po_items():
    if purchase_orders is None or items is None:
        print("Required databases not initialized.")
        return

    po_id = get_po_number()
    po_instance = purchase_orders.db.get(po_id)

    if po_instance is not None:
        # get_po_item_qdata returns (header, lines)
        header_lines = get_po_item_qdata(po_instance, items)

        if header_lines:
            header = header_lines.pop(0)
            lines = header_lines
            show_table(header, lines, f"PO {po_id} Items")
        else:
            print("No items found for this Purchase Order.")
    else:
        print("PO number not in database.")


def op_exit():
    print("Bye.")
    sys.exit()
