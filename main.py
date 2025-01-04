from pprint import pprint
from class_Database import IndivEntity, LegalEntity, Item, PurchaseOrder, Database
from prompts import VALID_ENTITIES, VALID_ITEMS_IDS_NAMES, confirm
from prompts import get_operation, get_po_number
from visualization import show_table
from functions import get_invoice_data, get_po_item_qdata, get_invoice_price
from pdf_creator import create_pdf
from email_service import send_email
import sys


def update_valid_lists():
    for entity in entities.db.values():
        if isinstance(entity, IndivEntity):
            VALID_ENTITIES.update({entity._entity_id: entity.last_name})
        elif isinstance(entity, LegalEntity):
            VALID_ENTITIES.update({entity._entity_id: entity.company_name})
        else:
            raise ValueError("Unknown entity type")
    for item in items.db.values():
        VALID_ITEMS_IDS_NAMES.update({item._item_id: item.item_name})


def database_initialization() -> object:
    global items
    items = Database(db_type="Item")
    items.load_db()
    global entities
    entities = Database(db_type="Entity")
    entities.load_db()
    # fulling the lists with valid entities and items
    update_valid_lists()
    global purchase_orders
    purchase_orders = Database(db_type="PurchaseOrder")
    purchase_orders.load_db()


def database_debug() -> None:
    """Debug"""
    pprint(items.db)
    print(type(items.db[1]._valid))
    pprint(entities.db)
    print(VALID_ENTITIES)
    print(VALID_ITEMS_IDS_NAMES)
    pprint(purchase_orders.db)
    print("End of debug output")


def add_i_to_db(db) -> None:
    try:
        db.add_to_db()
    except Exception as e:
        print(f"Exception {e} occured.")
    db.store_db()


def create_invoice(po_id) -> None:
    invoice_id = po_id
    try:
        purchase_orders.db[po_id].create_invoice(invoice_id)
        purchase_orders.store_db()
    except Exception:
        print("Send invoice anyway?")
        if confirm() == True:
            send_invoice(po_id)
        else:
            return


def send_invoice(po_id) -> None:
    file_name = f"Invoice {po_id:06d}"
    data = get_invoice_data(purchase_orders.db[po_id], items, entities)
    # pprint(data)  # debug
    create_pdf(data, file_name)
    customer = entities.db[purchase_orders.db[po_id]._customer_id]
    to_mail = customer.email
    subject = f"Invoice no. {data["invoice_id"]}"
    file_name = f"{file_name}.pdf"
    attachment_path = f"PDF_invoice\\{file_name}"
    try:
        send_email(
        to_email=to_mail,
        subject=subject,
        filename=file_name,
        attachment_path=attachment_path,
        body = "Dear customer,\n\nPlease find the invoice to your Purchase order in the attachement.\n\nBest regards,"
        )
    except Exception as e:
        print(f"Exception {e} occured.")


def show_all_db_i(db) -> None:
    """Shows all database item's values as a table,
    db example: purchase_orders.db"""
    lines = []
    header = db[1].get_header()
    for i in db.keys():
        line = db[i].get_i_data(entities)
        lines += line
    show_table(header, lines, "Show all db items")


def show_db_i(db_item)-> None:
    """Shows database item's values as a table,
    db_item example: purchase_orders.db[1]"""
    header = db_item.get_header()
    line = db_item.get_po_data()
    show_table(header, line, "Show db item")


def primary_screen() -> None:
    while True:
        operation = get_operation()
        operation = operation["operation"]

        if operation == "1":
            entities.add_to_db()
            entities.store_db()
            update_valid_lists()
        elif operation == "2":
            items.add_to_db()
            items.store_db()
            update_valid_lists()
        elif operation == "3":
            purchase_orders.add_to_db()
            purchase_orders.store_db()
        elif operation == "4":
            print("Choose PO number from the list:")
            show_all_db_i(purchase_orders.db)
            po_id = get_po_number()
            if po_id in purchase_orders.db.keys():
                # creates and sends the invoice
                create_invoice(po_id)
            else:
                print("PO number not in database.")
        elif operation == "5":
            show_all_db_i(entities.db)
        elif operation == "6":
            show_all_db_i(items.db)
        elif operation == "7":
            show_all_db_i(purchase_orders.db)
        elif operation == "8":
            po_id = get_po_number()
            if po_id in purchase_orders.db.keys():
                show_table(get_po_item_qdata(purchase_orders.db[po_id], items))
            else:
                print("PO number not in database.")
        elif operation == "9":
            print("Bye.")
            sys.exit()
        else:
            sys.exit("Unknown operation.")


def main():
    database_initialization()
    # database_debug()      # debug
    primary_screen()



if __name__ == "__main__":
    main()
