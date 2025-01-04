# from database import IndivEntity, LegalEntity, Item, PurchaseOrder, Database
from typing import Dict, List
from datetime import date, timedelta


def get_invoice_data(po, items, entities) -> Dict:
    """Return data for invoice displaying"""
    data = {}
    data["invoice_id"] = po._invoice_id
    data["invoice_date"] = po.invoice_issue_date
    data["po_id"] = po._po_id
    data["customer_addr"] = get_ent_addr(entities.db[(po.customer_id)])
    data["seller_addr"] = get_ent_addr(entities.db[(po.seller_id)])
    data["po_item_data"] = get_po_item_qdata(po, items)
    data["invoice_price"] = get_invoice_price(po, items)
    data["due_date"] = po.invoice_issue_date + timedelta(days=po.maturity)
    return data


def get_ent_addr(entity) -> List:
    """Return address of the entity"""
    addr = []
    addr = entity.get_name() + entity.get_adress()
    if entity.ent_type == "LegalEntity":
        addr += entity.get_company_data()
    return addr


def get_po_item_qdata(po, items) -> List:
    """
    Returns purchased items data for purchased q-ty
    po example purchase_orders.db[1]
    items is obj of class Item
    """
    po_item_data = []
    po_item_data += items.db[1].get_header()
    for i in po.purchased_items:
        item = items.db[(i["item_id"])]
        line = item.get_item_qdata(i["item_q_ty"])
        po_item_data += line
    return po_item_data


def get_invoice_price(po, items) -> Dict:
    """
    Returns total invoice values: total netto, VAT, Brutto
    po example purchase_orders.db[1]
    items is obj of class Item
    """
    total_netto = 0
    total_vat = 0
    total_brutto = 0
    for i in po.purchased_items:
        item = items.db[(i["item_id"])]
        q_ty = i["item_q_ty"]
        purchase_data = item.item_purchase_data(q_ty)
        total_netto += purchase_data["item_netto"]
        total_vat += purchase_data["item_vat"]
        total_brutto += purchase_data["item_brutto"]
    return {
        "total_netto": total_netto,
        "total_vat": total_vat,
        "total_brutto": total_brutto,
    }
