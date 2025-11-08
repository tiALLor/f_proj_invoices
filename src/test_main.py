import pytest
from datetime import date
from .classes.class_Database import (
    IndivEntity,
    LegalEntity,
    Item,
    PurchaseOrder,
    Database,
)
from global_data import VALID_ENTITIES, VALID_ITEMS_IDS_NAMES
from data_formatting import get_invoice_price, get_invoice_data

# Use a scope for the database instances, although global works for a simple test file
# The `Database` class likely uses a backing field name like `initial_db_type`
items = Database(initial_db_type="Item")
entities = Database(initial_db_type="Entity")
purchase_orders = Database(initial_db_type="PurchaseOrder")


def update_valid_lists():
    """Updates global lists used for item/entity validation."""
    VALID_ENTITIES.clear()
    VALID_ITEMS_IDS_NAMES.clear()

    for entity in entities.db.values():
        if entity is None:
            continue
        if isinstance(entity, IndivEntity):
            VALID_ENTITIES.update({entity._entity_id: entity.last_name})
        elif isinstance(entity, LegalEntity):
            VALID_ENTITIES.update({entity._entity_id: entity.company_name})
        # Assuming all entities are one of the above types based on your class structure.

    for item in items.db.values():
        if item is not None and isinstance(item, Item):
            VALID_ITEMS_IDS_NAMES.update({item._item_id: item.item_name})


# --- Setup Data ---

items.add_to_db(
    Item(
        _item_id=1,
        item_name="Screw",
        item_description="M5x20",
        item_unit="pcs",
        _price_per_unit=0.1,
        _vat_category="general",
    )
)
items.add_to_db(
    Item(
        _item_id=2,
        item_name="Nut",
        item_description="M5",
        item_unit="pcs",
        _price_per_unit=0.2,
        _vat_category="general",
    )
)

entities.add_to_db(
    LegalEntity(
        _entity_id=1,
        street_number="Aludarių g. 3",
        city="Vilnius",
        country="Lithuania",
        postal_code="LT-LT-01113",
        email="study@turingcollege.com",
        phone_no="123456789",
        company_name="Turing College",
        tax_id="LT47395850",
        vat_id="4739585",
        bank_account="RO13 RZBR 0000 0600 0713 4800",
        ent_type="LegalEntity",
    )
)
entities.add_to_db(
    IndivEntity(
        _entity_id=2,
        street_number="Ferenc Liszt 5",
        city="Warsaw",
        country="Poland",
        postal_code="00-000",
        email="JognDoe@gmail.com",
        phone_no="123456789",
        first_name="John",
        second_name="None",
        last_name="Doe",
        ent_type="IndivEntity",
    )
)
update_valid_lists()

purchase_orders.add_to_db(
    PurchaseOrder(
        _po_id=1,
        _order_date=date.fromisoformat("2024-12-31"),  # date object
        _customer_id=2,
        _invoice_issue_date=date.fromisoformat("2025-01-01"),  # date object
        _invoice_id=1,
        _seller_id=1,
        _purchased_items=[
            {"item_id": 1, "item_q_ty": 20},
            {"item_id": 2, "item_q_ty": 10},
        ],
        maturity=14,
    )
)

# --- Test Functions ---


def test_get_invoice_price():
    """Tests the total price calculation for a PurchaseOrder."""
    # Use pytest.approx for floating point comparisons
    expected = {
        "total_netto": 4.0,
        "total_vat": 0.84,
        "total_brutto": 4.84,
    }
    result = get_invoice_price(purchase_orders.db[1], items)

    assert result["total_netto"] == pytest.approx(expected["total_netto"])
    assert result["total_vat"] == pytest.approx(expected["total_vat"])
    assert result["total_brutto"] == pytest.approx(expected["total_brutto"])


def test_item_purchase_data():
    """Tests individual item calculation."""
    # Test non-zero quantity
    expected_40 = {
        "item_netto": 4.0,
        "vat_perc": 21.0,  # VAT_CATEGORIES.get should return float/int
        "item_vat": 0.84,
        "item_brutto": 4.84,
    }
    result_40 = items.db[1].item_purchase_data(40)  # type: ignore

    for key in expected_40:
        assert result_40[key] == pytest.approx(expected_40[key])

    # Test zero quantity
    assert items.db[1].item_purchase_data(0) == {  # type: ignore
        "item_netto": 0.0,
        "vat_perc": 21.0,
        "item_vat": 0.0,
        "item_brutto": 0.0,
    }


def test_get_invoice_data():
    """Tests invoice data structure and due date calculation."""
    data = get_invoice_data(purchase_orders.db[1], items, entities)

    print(data)

    # Due date should be Invoice Issue Date + Maturity (2025-01-01 + 14 days)
    assert data["due_date"] == date(2025, 1, 15)

    # Optional: Test key fields exist
    assert "invoice_id" in data
    assert "po_item_data" in data
    assert data["invoice_id"] == 1
