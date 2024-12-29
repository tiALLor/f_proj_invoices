from pprint import pprint
from database import IndivEntity, LegalEntity, Item, PurchaseOrder, Invoice, Database

def main():
    items = Database(db_type="Item")

    items.add_to_db(Item(1, "Screw", "M5x20", "pcs", 0.1, "general"))
    items.add_to_db(Item(2, "Nut", "M5", "pcs", 0.2, "general"))
    pprint(items.db)
    items.add_to_db()
    pprint(items.db)







if __name__ == "__main__":
    main()