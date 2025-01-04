import pytest
import pprint
from main import Database, Item, LegalEntity, IndivEntity, PurchaseOrder
from prompts import VALID_ENTITIES, VALID_ITEMS_IDS_NAMES
# from main import update_valid_lists, database_debug
from functions import get_invoice_price, get_invoice_data
from datetime import date

global items
items = Database(db_type="Item")
global entities
entities = Database(db_type="Entity")
global	purchase_orders
purchase_orders = Database(db_type="PurchaseOrder")

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

items.add_to_db(Item(1, "Screw", "M5x20", "pcs", 0.1, "general"))
items.add_to_db(Item(2, "Nut", "M5", "pcs", 0.2, "general"))

entities.add_to_db(
    LegalEntity(
        1,
        "Aludarių g. 3",
        "Vilnius",
        "Lithuania",
        "LT-LT-01113",
        "study@turingcollege.com",
        "123456789",
        "Turing College",
        "LT47395850",
        "4739585",
        "RO13 RZBR 0000 0600 0713 4800",
    )
)
entities.add_to_db(
    IndivEntity(
        2,
        "Ferenc Liszt 5",
        "Warsaw",
        "Poland",
        "00-000",
        "JognDoe@gmail.com",
        "123456789",
        "John",
        None,
        "Doe",
    )
)
update_valid_lists()


purchase_orders.add_to_db(PurchaseOrder(
    1, "2024-12-31", 2, 1,
    [{"item_id": 1,"item_q_ty": 20}, {"item_id": 2,"item_q_ty": 10}], 1, date(2025, 1, 1), 14
))


def test_get_invoice_price():
    assert get_invoice_price(purchase_orders.db[1], items) == {
        "total_netto": 4.0,
        "total_vat": 0.84,
        "total_brutto": 4.84,
    }

def test_item_purchase_data():
    assert items.db[1].item_purchase_data(40) == {
        "item_netto": 4.0,
        "vat_perc": 21,
        "item_vat": 0.84,
        "item_brutto": 4.84,
    }
    assert items.db[1].item_purchase_data(0) == {
        "item_netto": 0,
        "vat_perc": 21,
        "item_vat": 0,
        "item_brutto": 0,
    }

def test_get_invoice_data():
    data = get_invoice_data(purchase_orders.db[1], items, entities)
    assert data["due_date"] == date(2025, 1, 15)
