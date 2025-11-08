from typing import Dict, Any, Callable, Union, Tuple

# Define a type alias for the common parser return signature: (id, data, entity_type/placeholder)
ParserResult = Tuple[int, Dict[str, Any], Union[str, int]]


def item_parser(row: Dict[str, Any]) -> ParserResult:
    """Parses a dictionary row into item data, converting types."""
    data = {
        "_item_id": int(row["_item_id"]),
        "item_name": row["item_name"],
        "item_description": row["item_description"],
        "item_unit": row["item_unit"],
        "_price_per_unit": float(row["price_per_unit"]),
        "_vat_category": row["vat_category"],
        "_valid": bool(row["_valid"]),
        "_currency": row["_currency"],
    }
    # Placeholder for entity type is 0
    return data["_item_id"], data, 0


def legal_entity_parser(row: Dict[str, Any]) -> ParserResult:
    """Parses a dictionary row into legal entity data, converting types."""
    data = {
        "_entity_id": int(row["_entity_id"]),
        "street_number": row["street_number"],
        "city": row["city"],
        "country": row["country"],
        "postal_code": row["postal_code"],
        "email": row["email"],
        "phone_no": row["phone_no"],
        "ent_type": row["ent_type"],
        "company_name": row["company_name"],
        "vat_id": row["vat_id"],
        "tax_id": row["tax_id"],
        "bank_account": row["bank_account"],
    }
    return data["_entity_id"], data, "LegalEntity"


def private_entity_parser(row: Dict[str, Any]) -> ParserResult:
    """Parses a dictionary row into individual entity data, converting types."""
    data = {
        "_entity_id": int(row["_entity_id"]),
        "street_number": row["street_number"],
        "city": row["city"],
        "country": row["country"],
        "postal_code": row["postal_code"],
        "email": row["email"],
        "phone_no": row["phone_no"],
        "ent_type": row["ent_type"],
        "first_name": row["first_name"],
        "second_name": row["second_name"],
        "last_name": row["last_name"],
    }
    return data["_entity_id"], data, "IndivEntity"


def purchase_order_parser(row: Dict[str, Any]) -> ParserResult:
    """Parses a dictionary row into purchase order data, handling date/json conversion."""

    # Safely handle issue date being 0 or an ISO string
    issue_date = row.get("invoice_issue_date", 0)
    parsed_issue_date: Union[int, str]

    if issue_date == 0:
        parsed_issue_date = 0
    else:
        # date is stored as ISO format string
        parsed_issue_date = str(issue_date)

    data = {
        "_po_id": int(row["_po_id"]),
        "_order_date": str(row["order_date"]),  # Ensure date is handled as a string
        "_customer_id": int(row["customer_id"]),
        "_seller_id": int(row["seller_id"]),
        "_purchased_items": row["purchased_items"],
        "_invoice_id": int(row["_invoice_id"]),
        # TODO check why its a date value
        "_invoice_issue_date": parsed_issue_date,
        "maturity": int(row["maturity"]),
    }
    return data["_po_id"], data, 0


def parse(row: Dict[str, Any], db_type: str) -> Union[ParserResult, None]:
    """
    Selects and executes the correct parser based on db_type.

    :param row: Dictionary containing database row data.
    :param db_type: The type of database object ("Entity", "Item", "PurchaseOrder").
    :return: ParserResult tuple (id, data_dict, type) or None if db_type is unsupported.
    """

    parser: Union[Callable[[Dict], ParserResult], None] = None

    if db_type == "Entity":
        entity_type = row.get("ent_type")
        if entity_type == "LegalEntity":
            parser = legal_entity_parser
        elif entity_type == "IndivEntity":
            parser = private_entity_parser
        else:
            raise ValueError(f"Invalid entity type: {entity_type} for db_type=Entity")

    elif db_type == "Item":
        parser = item_parser

    elif db_type == "PurchaseOrder":
        parser = purchase_order_parser

    else:
        # Handle unsupported db_type explicitly
        return None

    # Check if parser was assigned (not None) before calling
    if parser is None:
        # This branch should theoretically only be hit if a new db_type is added
        # without updating the condition, but acts as a final safety check.
        return None

    return parser(row)
