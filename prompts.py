import inquirer
from validators import iban_is_valid, valid_number, valid_mail
from typing import List, Dict
from pprint import pprint


def db_item_creator(item_class:str, id:int, **kwargs) -> dict:
    if item_class == "IndivEntity":
        pass
    elif item_class == "LegalEntity":
        pass
    elif item_class == "Item":
        print("======\nMode: Provide item data to store item into database: \n")
        o = inquirer.prompt(q_item)
        o["_item_id"] = id
        pprint(o)
        print("======\n")
        if True in inquirer.prompt(q_confirm).values():
            return o
        else:
            return None

    elif item_class == "PurchaseOrder":
        db_ids = kwargs.get("db_ids")
        db_names = kwargs.get("db_names")
        db = {}
        while True:
            o = purchase_order_creator(db_ids, db_names)
            db.update(o)
            inquirer.prompt(inquirer.Confirm(
                "Add another item to purchase order?", default=True))
        return o
    elif item_class == "Invoice":
        pass

def purchase_order_creator(db_ids: List[int], db_names: List[str]) -> Dict:
    q_add_item_to_po = [
        inquirer.List("item_ID", message="Item ID to be purchased: ",
                        choices=db_ids, hints=db_names , other=True, carousel=True),
        inquirer.Text("q_ty", message="Quantity of item units: ",
                        validate=valid_number),
    ]
    for i, q in inquirer.prompt(q_add_item_to_po).items():
        return {i:q}

VAT_CATEGORIES: Dict[str, int] = {
    "food": 5,
    "books": 10,
    "servicies": 21,
    "generall": 21,
    "accomendations": 10,
}

item_units = ["pcs", "m", "m2", "m3", "sets", "liters"]


q_indiv_entity = [
    inquirer.Text("name_first", message="Fist name: ",
                    validate=lambda _, x: x != ""),
    inquirer.Text("name_second", message="Middle name: ",
                    validate=lambda _, x: x != "", default="None"),
    inquirer.Text("name_last", message="Last name: ",
                    validate=lambda _, x: x != ""),
]

q_legal_entity = [
    inquirer.Text("name_company", message="Fist name: ",
                    validate=lambda _, x: x != ""),
    inquirer.Text("vat_id", message="VAT number: ",
                    validate=lambda _, x: x != ""),
    inquirer.Text("tax_id", message="TAX number: ",
                    validate=lambda _, x: x != ""),
    inquirer.Text("bank_account", message="Bank account number: ",
                    validate= iban_is_valid, default="None"),
]

q_entity = [
    inquirer.Text("street_number", message="Streer and house number: ",
                    validate=lambda _, x: x != ""),
    inquirer.Text("city", message="City: ", validate=lambda _, x: x != ""),
    inquirer.Text("country", message="Country: ", validate=lambda _, x: x != ""),
    inquirer.Text("postal_code", message="Postal code: ",
                    validate=lambda _, x: x != ""),
    inquirer.Text("phone_no", message="Phone number: ",
                    validate=lambda _, x: x != "", default="None"),
    inquirer.Text("email", message="E-mail: ", validate=valid_mail),
]


q_item = [
    inquirer.Text("item_name", message="Item name: ", validate=lambda _, x: x != ""),
    inquirer.Text("item_decription", message="Item decription (optional): ",
                    validate=lambda _, x: x != "", default="None"),
    inquirer.List("item_unit", message="Item unit: ",
                    choices=item_units, carousel=True),
    inquirer.Text("price_per_unit", message="Price per unit: ",
                    validate=valid_number),
    inquirer.List("vat_category", message="VAT category: ", choices=VAT_CATEGORIES.keys(), default="generall", carousel=True),
]

q_confirm = [
    inquirer.Confirm("confirm", message="Confirm the action?", default=True)
]