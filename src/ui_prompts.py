import inquirer
from typing import List, Dict, Any, Union, Tuple
from pprint import pprint
from datetime import date
from .prompts.query_builder import query_builder
from .prompts.prompt_data import (
    confirm_question_data,
    entity_type_question_data,
    entity_questions_data,
    indiv_entity_question_data,
    legal_entity_question_data,
    item_question_data,
    purchase_order_question_data,
    purchase_item_question_data,
    invoice_question_data,
    get_operation_question_data,
    get_po_number_question_data,
)
from global_data import (
    VALID_ITEMS_IDS_NAMES,
    VALID_ENTITIES,
)

# Define a type alias for the return value of inquirer.prompt
Answers = Dict[str, Any]

# --- Functions with Type Hints and Simplification ---


def confirm() -> bool:
    """Confirms an action with the user."""
    answers: Answers = inquirer.prompt(query_builder(confirm_question_data))
    return answers.get("confirm", False)


def entity_creator() -> Tuple[Answers, str]:
    """Prompts the user for entity type and then relevant data."""
    print(
        "======\nMode: Provide entity's data to store the entity (e.g. customer) into database:\n"
    )

    choice: Answers = inquirer.prompt(query_builder(entity_type_question_data))
    ent_type: str = choice.get("entity_type", "")

    if ent_type == "IndivEntity":
        # Concatenate questions for individual entity
        data: Answers = inquirer.prompt(
            query_builder(indiv_entity_question_data + entity_questions_data)
        )
    elif ent_type == "LegalEntity":
        # Concatenate questions for legal entity
        data: Answers = inquirer.prompt(
            query_builder(legal_entity_question_data + entity_questions_data)
        )
    else:
        # Should not happen if entity_type is a List question, but good practice
        raise ValueError(f"Unknown entity type: {ent_type}")

    return data, ent_type


def get_purchased_items() -> List[Dict[str, int]]:
    """Allows user to repeatedly add items and quantities to a list."""
    purchased_items: List[Dict[str, int]] = []
    while True:
        # Debug statements are kept for context
        print(VALID_ITEMS_IDS_NAMES)

        answers: Answers = inquirer.prompt(query_builder(purchase_item_question_data))

        # Convert inputs to required integer types immediately
        item_id: int = int(answers.get("item_ID", 0))
        quantity: int = int(
            float(answers.get("q_ty", 0))
        )  # Use float() then int() to handle valid_number output

        purchased_items.append({"item_id": item_id, "item_q_ty": quantity})

        q: Answers = inquirer.prompt(
            [
                inquirer.Confirm(
                    "more", message="Add another item to purchase order?", default=True
                )
            ]
        )
        if not q["more"]:
            break

    return purchased_items


def purchase_order_creator() -> Answers:
    """Prompts for PO data, customer ID, and calls for item list."""
    print("======\nMode: Provide PO's data to store the PO into database:\n")
    print(VALID_ENTITIES)

    data: Answers = inquirer.prompt(query_builder(purchase_order_question_data))

    # Convert customer_id to int immediately
    data["customer_id"] = int(data.get("customer_id", 0))

    data["purchased_items"] = get_purchased_items()
    data["order_date"] = date.today().isoformat()

    return data


def db_i_creator(db_i_class: str, id: int) -> Union[Tuple[Answers, str], None]:
    """
    Master function to create data for various database classes.

    :param db_i_class: The class type being created ("Entity", "Item", "PurchaseOrder", "Invoice").
    :param id: The ID to be assigned to the new object.
    :return: A tuple (data_dictionary, entity_type) if successful, or None.
    """

    # Initialize variables for safe return
    o: Answers = {}
    ent_type: str = "N/A"

    if db_i_class == "Entity":
        # entity_creator returns (Answers, str)
        o, ent_type = entity_creator()
        o["_entity_id"] = id

    elif db_i_class == "Item":
        print("======\nMode: Provide item's data to store the item into database: \n")
        o = inquirer.prompt(query_builder(item_question_data))
        o["_item_id"] = id

    elif db_i_class == "PurchaseOrder":
        o = purchase_order_creator()
        o["_po_id"] = id

    elif db_i_class == "Invoice":
        o = invoice()

    # Check if a dictionary was successfully created/populated
    if not o:  # Allow empty dict for Invoice case which was passed
        return None

    pprint(o)
    print("======\n")

    if confirm():
        if db_i_class == "Entity":
            return o, ent_type
    else:
        return None


def invoice() -> Answers:
    """Prompts for invoice creation data."""
    print("\nMode: Provide data to create a invoice:")
    data: Answers = inquirer.prompt(query_builder(invoice_question_data))

    # Convert maturity to int (valid_number ensures it's a numeric string)
    data["maturity"] = int(float(data.get("maturity", 0)))

    # The date should be stored as an ISO string usually, but if you need a date object:
    data["invoice_issue_date"] = date.fromisoformat(data["invoice_issue_date"])

    return data


def get_operation() -> str:
    """Gets the user's choice for the next operation."""
    answers: Answers = inquirer.prompt(query_builder(get_operation_question_data))
    # The return value of a List question is the value, not the label
    return answers.get("operation", "")


def get_po_number() -> int:
    """Prompts the user for a PO ID and validates it as a number."""
    answers: Answers = inquirer.prompt(query_builder(get_po_number_question_data))

    # Use float then int to handle valid_number output
    return int(float(answers.get("po_id", 0)))
