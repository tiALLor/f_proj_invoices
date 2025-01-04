from abc import ABC, abstractmethod
from dataclasses import dataclass, field, asdict
from typing import List, Dict, Any
from datetime import date
from prompts import db_i_creator, invoice, VAT_CATEGORIES
from prompts import VALID_ENTITIES, VALID_ITEMS_IDS_NAMES
from class_Item import Item
from class_Entity import Entity, LegalEntity, IndivEntity
from class_PurchaseOrder import PurchaseOrder
from enum import StrEnum
from parsers import parse
import json
import csv
import sys


@dataclass
class Database:
    """Database class for storing Items, Entities, PurchaseOrders, Invoces"""

    db_type: str
    db: Dict[int, Item | Entity | PurchaseOrder] = field(default_factory=dict)

    files = {
        "Item": "databases/database_items.json",
        "Entity": "databases/database_entities.json",
        "PurchaseOrder": "databases/databese_POs.json",
    }
    class_map = {
        "Item": Item,
        "Entity": Entity,
        "IndivEntity": IndivEntity,
        "LegalEntity": LegalEntity,
        "PurchaseOrder": PurchaseOrder,
    }

    def add_to_db(self, db_i=0, id=0) -> None:
        """Adds item to database, id = no. of the item, db_i are the values"""
        if id == 0:
            id = self.max_id()
        if db_i == 0:
            data, ent_type = db_i_creator(self.db_type, id)
            if data:
                db_i = self.db_class_type(ent_type)(**data)
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
        """Return a list of used values for given attribute name"""
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
                    json.dump(self.db, f, default=lambda x: x.serialize(), indent=4)
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
                        print(data)
                        db_i = self.db_class_type(ent_type)(**data)
                        self.db[id] = db_i
        except Exception as e:
            print(f"Exception {e} occurred!")
            sys.exit()
        print(f"Database loaded from file {file_name}")

        @property
        def db_type(self) -> str:
            return self._db_type

        @db_type.setter
        def db_type(self, value: str) -> None:
            if value not in self.files.keys():
                raise ValueError("Invalid db_type")
            self._db_type = value
