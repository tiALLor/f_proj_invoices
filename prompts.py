import inquirer
from validators import iban_is_valid, valid_number, valid_mail
from typing import List, Dict
from pprint import pprint


def db_i_creator(db_i_class: str, id: int) -> tuple:
    if db_i_class == "Entity":
        o, ent_type = entity_creator()
        o["_entity_id"] = id
    elif db_i_class == "LegalEntity":
        pass
    elif db_i_class == "Item":
        print("======\nMode: Provide item's data to store the item into database: \n")
        o = inquirer.prompt(q_item)
        o["_item_id"] = id


    elif db_i_class == "PurchaseOrder":
        db = {}
        while True:
            o = purchase_order_creator(VALID_ITEMS_IDS, VALID_ITEM_NAMES)
            db.update(o)
            inquirer.prompt(
                inquirer.Confirm("Add another item to purchase order?", default=True)
            )
        return o
        ...
    elif db_i_class == "Invoice":
        pass
    pprint(o)       # debug
    print("======\n")
    if True in inquirer.prompt(q_confirm).values():
        return o, ent_type if db_i_class == "Entity" else 0
    else:
        return None
    


def entity_creator() -> tuple:
    print("""
          ======\nMode: Provide entity's data to store the entity
          (e.g. customer) into database:\n
          """)
    choice = inquirer.prompt(q_entity_type)
    if choice["entity_type"] == "IndivEntity":
        o = inquirer.prompt(q_indiv_entity + q_entity)
        ent_type = "IndivEntity"
    elif choice["entity_type"] == "LegalEntity":
        o = inquirer.prompt(q_legal_entity + q_entity)
        ent_type = "LegalEntity"
    return o, ent_type
    

def purchase_order_creator(VALID_ITEMS_IDS: List[int], VALID_ITEM_NAMES: List[str]) -> Dict:
    q_add_item_to_po = [
        inquirer.List(
            "item_ID",
            message="Item ID to be purchased",
            choices=VALID_ITEMS_IDS,   
            hints=VALID_ITEM_NAMES,   
            other=True,
            carousel=True,
        ),
        inquirer.Text("q_ty", message="Quantity of item units", validate=valid_number),
    ]
    for i, q in inquirer.prompt(q_add_item_to_po).items():
        return {i: q}


VAT_CATEGORIES: Dict[str, int] = {
    "food": 5,
    "books": 10,
    "servicies": 21,
    "general": 21,
    "accomendations": 10,
}

item_units = ["pcs", "m", "m2", "m3", "sets", "liters"]


VALID_ENTITIES = []
'''Stores valid entity_ids from the database entities.db to be used for validation'''

VALID_ITEMS_IDS = []
'''Stores valid item_ids from the database items.db to be used for validation'''

VALID_ITEM_NAMES = []
'''Stores valid item names from the database items.db to be used for validation'''





q_indiv_entity = [
    inquirer.Text("first_name", message="First name", validate=lambda _, x: x != ""),
    inquirer.Text(
        "second_name",
        message="Middle name (optional)",
        validate=lambda _, x: x != "",
        default="None",
    ),
    inquirer.Text("last_name", message="Last name", validate=lambda _, x: x != ""),
]

q_legal_entity = [
    inquirer.Text("company_name", message="Company's name", validate=lambda _, x: x != ""),
    inquirer.Text("vat_id", message="VAT number", validate=lambda _, x: x != ""),
    inquirer.Text("tax_id", message="TAX number", validate=lambda _, x: x != ""),
    inquirer.Text(
        "bank_account",
        message="Bank account number",
        validate=iban_is_valid,
        default="None",
    ),
]

q_entity = [
    inquirer.Text(
        "street_number",
        message="Streer and house number",
        validate=lambda _, x: x != "",
    ),
    inquirer.Text("city", message="City", validate=lambda _, x: x != ""),
    inquirer.Text("country", message="Country", validate=lambda _, x: x != ""),
    inquirer.Text(
        "postal_code", message="Postal code", validate=lambda _, x: x != ""
    ),
    inquirer.Text(
        "phone_no",
        message="Phone number",
        validate=lambda _, x: x != "",
        default="None",
    ),
    inquirer.Text("email", message="E-mail", validate=valid_mail),
]


q_item = [
    inquirer.Text("item_name", message="Item name", validate=lambda _, x: x != ""),
    inquirer.Text(
        "item_decription",
        message="Item decription (optional)",
        validate=lambda _, x: x != "",
        default="None",
    ),
    inquirer.List(
        "item_unit", message="Item unit", choices=item_units, carousel=True
    ),
    inquirer.Text(
        "price_per_unit",
        message="Price per unit [EUR] (without VAT)",
        validate=valid_number,
    ),
    inquirer.List(
        "vat_category",
        message="VAT category",
        choices=VAT_CATEGORIES.keys(),
        default="generall",
        carousel=True,
    ),
]


q_entity_type = [
    inquirer.List(
        "entity_type",
        message="Which entity (e.g. customer) type are you adding?",
        choices=["IndivEntity", "LegalEntity"],
        carousel=True,
    )
]

q_confirm = [inquirer.Confirm("confirm", message="Confirm the action?", default=True)]
