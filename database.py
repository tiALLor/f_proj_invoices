from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from typing import List, Dict
from datetime import date
from prompts import db_item_creator
from enum import StrEnum




@dataclass
class Entity:
    _entity_id: int
    street_number: str
    city: str
    country: str
    postal_code: str
    email: str
    phone_no: str


    
    # _id generator, unique number (enumerate)
    # email can not be empty, we need to send an mail
    # email need to be validated
    # factory???

@dataclass
class IndivEntity(Entity):
    name_first: str
    name_second: str
    name_last:  str

@dataclass
class LegalEntity(Entity):
    name_company: str
    vat_id: str
    tax_id: str
    bank_account: str


@dataclass
class Item:
    _item_id: int
    item_name:  str
    item_decription: str
    item_unit: str           # pcs, m, m2, m3, sets, liter
    price_per_unit: float
    vat_category: str          # food,  books, servicies, general
    _valid: bool = field(default=True)
    _currency: str = "EUR"



@dataclass
class PurchaseOrder:
    _order_no: int
    db: Dict["_item_id": int, "q_ty": int]
    date_order: date
    buyer_id: int
    seller_id: int
    _invoice_no: int

    # where I will store the POs?


@dataclass
class Invoice:
    _invoice_no: str
    date_issued: date
    date_due: date
    netto_value: float
    tax: float
    brutto_value: float
    _purchase_order_no: int

    # where I will store the Invoces?
    # PO need to exist
    # need to load items into the invoice
    # post_init for 
    # possibility to cancel invoice?

@dataclass
class Database:
    ''' Database class for storing Items, Entities, PurchaseOrders, Invoces '''
    
    db_type: str
    db: Dict[int, Item | Entity | PurchaseOrder | Invoice] = field(default_factory=dict)
    



    def add_to_db(self, item=0, id=0) -> None:
        if id == 0:
            id = self.max_id()
        if item == 0:
            data = db_item_creator(
                self.db_type,
                id,
                db_ids=self.db.keys(),
                db_names=self.get_items_att("item_name"))
            if data:
                item = self.db_class_type()(**data)
                self.db[id] = item
            else:
                print("======\nIterupted by user\n=======\n")
                return None
        self.db[id] = item

    def max_id(self) -> int:
        try:
            id = max(self.db.keys()) + 1
        except ValueError:
            """if database of questions is empty"""
            id = 1
        return id
    
    def get_items_att(self, item_att_name) -> List[int]:
        return [getattr(item, item_att_name) for item in self.db.values()]
        # return [item for item in self.db.keys() if isinstance(self.db[item], Item)]
    
    def db_class_type(self) -> type:
        class_map = {
            "Item": Item,
            "IndivEntity": IndivEntity,
            "LegalEntity": LegalEntity,
            "PurchaseOrder": PurchaseOrder,
            "Invoice": Invoice
        }
        return class_map.get(self.db_type)
    

    # list_of_ids()