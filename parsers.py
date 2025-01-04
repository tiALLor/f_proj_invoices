from typing import List, Dict
from datetime import date
import json


def parse(row: dict, db_type: str) -> Dict:
    if db_type == "Entity":
        if row["ent_type"] == "LegalEntity":
            parser = legal_entity_parser
        elif row["ent_type"] == "IndivEntity":
            parser = private_entity_parser
        else:
            raise ValueError("Invalid db entity type")
    elif db_type == "Item":
        parser = item_parser
    elif db_type == "PurchaseOrder":
        parser = purchase_order_parser
    if parser is None:
        return None
    return parser(row)


def item_parser(row: Dict) -> tuple:
    data = {
        "_item_id": int(row["_item_id"]),
        "item_name": row["item_name"],
        "item_decription": row["item_decription"],
        "item_unit": row["item_unit"],
        "price_per_unit": float(row["price_per_unit"]),
        "vat_category": row["vat_category"],
        "_valid": bool(row["_valid"]),
        "_currency": row["_currency"],
    }
    return data.get("_item_id"), data, 0


def legal_entity_parser(row: dict) -> tuple:
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
    return data.get("_entity_id"), data, "LegalEntity"


def private_entity_parser(row: dict) -> tuple:
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
    return data.get("_entity_id"), data, "IndivEntity"


def purchase_order_parser(row: dict) -> tuple:
    data = {
        "_po_id": int(row["_po_id"]),
        "order_date": (row["order_date"]),
        "customer_id": int(row["customer_id"]),
        "seller_id": int(row["seller_id"]),
        "purchased_items": (row["purchased_items"]),
        "_invoice_id": int(row["_invoice_id"]),
        "invoice_issue_date": 0
        if row["invoice_issue_date"] == 0
        else date.fromisoformat(row["invoice_issue_date"]),
        "maturity": int(row["maturity"]),
    }
    return data.get("_po_id"), data, 0
