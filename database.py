from abc import ABC, abstractmethod
from dataclasses import dataclass, field, asdict
from typing import List, Dict, Any
from datetime import date
from prompts import db_i_creator, VAT_CATEGORIES
from enum import StrEnum
from parsers import parse
import json
import csv
from prompts import VALID_ENTITIES, VALID_ITEMS_IDS, VALID_ITEM_NAMES



@dataclass
class Entity:
    _entity_id: int
    street_number: str
    city: str
    country: str
    postal_code: str
    email: str
    phone_no: str

    def serialize(self) -> dict:
        serialized = {
            "_entity_id": self._entity_id,
            "street_number": self.street_number,
            "city": self.city,
            "country": self.country,
            "postal_code": self.postal_code,
            "email": self.email,
            "phone_no": self.phone_no,
            "ent_type": self.ent_type,
        }
        serialized["first_name"] = (
            self.first_name if hasattr(self, "first_name") else "Empty"
        )
        serialized["second_name"] = (
            self.second_name if hasattr(self, "second_name") else "Empty"
        )
        serialized["last_name"] = (
            self.last_name if hasattr(self, "last_name") else "Empty"
        )
        serialized["company_name"] = (
            self.company_name if hasattr(self, "company_name") else "Empty"
        )
        serialized["vat_id"] = self.vat_id if hasattr(self, "vat_id") else "Empty"
        serialized["tax_id"] = self.tax_id if hasattr(self, "tax_id") else "Empty"
        serialized["bank_account"] = (
            self.bank_account if hasattr(self, "bank_account") else "Empty"
        )
        return serialized

    @classmethod
    def header(cls) -> List[str]:
        fields = []
        fields.extend(list(Entity.__annotations__.keys()))
        fields.extend(list(IndivEntity.__annotations__.keys()))
        fields.extend(list(LegalEntity.__annotations__.keys()))
        return fields


@dataclass
class IndivEntity(Entity):
    first_name: str
    second_name: str
    last_name: str
    ent_type: str = "IndivEntity"


@dataclass
class LegalEntity(Entity):
    company_name: str
    vat_id: str
    tax_id: str
    bank_account: str
    ent_type: str = "LegalEntity"
    # additional_attrs: Dict[str, Any] = field(default_factory=dict, init=False)

    # def __post_init__(self, **kwargs):
    #     # Store any additional keyword arguments in the additional_attrs dictionary
    #     self.additional_attrs = {k: v for k, v in kwargs.items() if k not in self.__annotations__}
    #     for k, v in self.additional_attrs.items():
    #         setattr(self, k, v)


@dataclass
class Item:
    _item_id: int
    item_name: str
    item_decription: str
    item_unit: str  # pcs, m, m2, m3, sets, liter
    price_per_unit: float
    vat_category: str  # food,  books, servicies, general
    _valid: bool = field(default=True)
    _currency: str = "EUR"

    @classmethod
    def header(cls) -> List[str]:
        return list(Item.__annotations__.keys())

    def serialize(self) -> dict:
        return asdict(self)
    
    @property
    def vat_category(self) -> str:
        return self._vat_category
    
    @vat_category.setter
    def vat_category(self, value: str) -> None:
        if value not in VAT_CATEGORIES.keys():
            raise ValueError("Invalid VAT category")
        self._vat_category = value
    
    @property
    def price_per_unit(self) -> float:
        return self._price_per_unit
    
    @price_per_unit.setter
    def price_per_unit(self, value: float) -> None:
        self._price_per_unit = float(value)

    @property
    def price_with_vat(self) -> float:
        vat = VAT_CATEGORIES.get(self.vat_category)
        return self.price_per_unit * (1 + vat / 100)

@dataclass
class PurchaseOrder:
    _order_no: int
    date_order: date
    buyer_id: int
    seller_id: int
    db: List[Dict[str, int]] = field(default_factory=list)
    _invoice_no: int = (field(default=0, init=False),)
    date_issued: date = field(default=0, init=False)
    maturity: int = field(default=14, init=False)  # user imput from payment terms

    @classmethod
    def header(cls) -> List[str]:
        return list(PurchaseOrder.__annotations__.keys())

    def serialize(self) -> dict:
        return asdict(self)
    
    @property
    def buyer_id(self) -> int:
        return self._buyer_id
    
    @buyer_id.setter
    def buyer_id(self, value: int) -> None:
        if value not in VALID_ENTITIES:
            raise ValueError("Invalid buyer ID")
        self._buyer_id = value

    @property
    def seller_id(self) -> int:
        return self._seller_id
    
    @seller_id.setter
    def seller_id(self, value: int) -> None:
        if value not in VALID_ENTITIES:
            raise ValueError("Invalid seller ID")
        self._seller_id = value


# @dataclass
# class Invoice:
#     _invoice_no: str
#     date_issued: date       # conversion to date object, how to handle it?
#     date_due: date          # user imput from payment terms
#     netto_value: float      # calculated
#     tax: float              # calculated
#     brutto_value: float     # calculated
#     _purchase_order_no: int

#     def header(self) -> List[str]:
#         return list(Invoice.__annotations__.keys())

#     def serialize(self) -> dict:
#         return asdict(self)

#     def parser(self, row: dict) -> Dict:
#         data = {
#             "_invoice_no": row["_invoice_no"],
#             "date_issued": row["date_issued"],
#             "date_due": row["date_due"],
#             "netto_value": float(row["netto_value"]),
#             "tax": float(row["tax"]),
#             "brutto_value": float(row["brutto_value"]),
#             "_purchase_order_no": int(row["_purchase_order_no"]),
#         }
#         return data


#     # PO need to exist
#     # need to load items into the invoice
#     # post_init for
#     # possibility to cancel invoice?


@dataclass
class Database:
    """Database class for storing Items, Entities, PurchaseOrders, Invoces"""

    db_type: str
    db: Dict[int, Item | Entity | PurchaseOrder] = field(default_factory=dict)

    files = {
        "Item": "database_items.json",
        "Entity": "database_entities.json",
        "PurchaseOrder": "databese_POs.json",
    }
    class_map = {
        "Item": Item,
        "Entity": Entity,
        "IndivEntity": IndivEntity,
        "LegalEntity": LegalEntity,
        "PurchaseOrder": PurchaseOrder,
    }

    def add_to_db(self, db_i=0, id=0) -> None:
        if id == 0:
            id = self.max_id()
        if db_i == 0:
            data, ent_type = db_i_creator(
                self.db_type,
                id,
                # db_ids=self.db.keys(),
                # db_names=self.get_db_i_att("item_name"),
            )
            if data:
                db_i = self.db_class_type(ent_type)(**data)
                self.db[id] = db_i
            else:
                print("======\nIterupted by user\n=======\n")
                return None
        self.db[id] = db_i

    def max_id(self) -> int:
        try:
            id = max(self.db.keys()) + 1
        except ValueError:
            """if database of questions is empty"""
            id = 1
        return id

    def get_db_i_att(self, db_i_att_name) -> List[int]:
        """Return a list of ussed values for given attribute name"""
        return [getattr(db_i, db_i_att_name) for db_i in self.db.values()]
        # return [db_i for db_i in self.db.keys() if isinstance(self.db[db_i], Item)]

    def db_class_type(self, ent_type=0) -> type:
        if ent_type == 0:
            return self.class_map.get(self.db_type)
        else:
            return self.class_map.get(ent_type)

    def store_db(self) -> None:
        """Store the database in a file"""
        file_name = self.files.get(self.db_type)
        print(file_name)
        file_format = file_name.split(".")[-1]
        file_format = file_format.upper()
        if file_format not in ["JSON", "CSV"]:
            print("File format not supported!")
            return None
        try:
            with open(file_name, "w", encoding="utf-8", newline="") as f:
                if file_format == "JSON":
                    json.dump(self.db, f, default=lambda x: x.serialize())
                elif file_format == "CSV":
                    writer = csv.DictWriter(f, fieldnames=self.db_class_type().header())
                    writer.writeheader()
                    for db_i in self.db.values():
                        writer.writerow(db_i.serialize())
        except Exception as e:
            print(f"Exception {e} occurred!")
            return None
        print("Database stored in file.\n")

    def load_db(self) -> None:
        """Load the database from a file"""
        file_name = self.files.get(self.db_type)
        file_format = file_name.split(".")[-1]
        file_format = file_format.upper()
        if file_format not in ["JSON", "CSV"]:
            print("File format not supported!")
            return None
        try:
            with open(file_name, "r") as f:
                if file_format == "JSON":
                    data = json.load(f)
                    for value in data.values():
                        id, data, ent_type = parse(value, self.db_type)
                        db_i = self.db_class_type(ent_type)(**data)
                        self.db[id] = db_i
                elif file_format == "CSV":
                    reader = csv.DictReader(f)
                    for row in reader:
                        id, data, ent_type = parse(row, self.db_type)
                        db_i = self.db_class_type(ent_type)(**data)
                        self.db[id] = db_i
        except Exception as e:
            print(f"Exception {e} occurred!")
            return None
        print("Database loaded from file.\n")

    # def list_of_ids()?
