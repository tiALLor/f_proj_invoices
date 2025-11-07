from dataclasses import dataclass, field
from typing import List, Dict, Any, Union, Literal, Type, Tuple
from ui_prompts import db_i_creator
from .class_Item import Item
from .class_Entity import Entity, LegalEntity, IndivEntity
from .class_PurchaseOrder import PurchaseOrder
from parsers import parse
import json
import csv
import sys

ValidDbTypes = Literal["Item", "Entity", "PurchaseOrder"]

Db = Dict[int, Union[Item, Entity, PurchaseOrder, None]]

# Define the acceptable class types for type checking
DbClassType = Union[
    Type[Item], Type[Entity], Type[LegalEntity], Type[IndivEntity], Type[PurchaseOrder]
]


@dataclass(
    kw_only=True
)  # Using kw_only=True forces fields without defaults to be set with keywords
class Database:
    """Database class for storing Items, Entities, PurchaseOrders, Invoices"""

    initial_db_type: ValidDbTypes

    files: Dict[Literal["Item", "Entity", "PurchaseOrder"], str] = field(
        default_factory=lambda: {
            "Item": "databases/database_items.json",
            "Entity": "databases/database_entities.json",
            "PurchaseOrder": "databases/database_POs.json",
        },
        init=False,  # Exclude from constructor
    )

    class_map: Dict[str, DbClassType] = field(
        default_factory=lambda: {
            "Item": Item,
            "Entity": Entity,  # Though not directly instantiated, kept for hierarchy
            "IndivEntity": IndivEntity,
            "LegalEntity": LegalEntity,
            "PurchaseOrder": PurchaseOrder,
        },
        init=False,  # Exclude from constructor
    )

    # The internal storage for the database type string
    _db_type: ValidDbTypes = field(init=False)

    db: Db = field(default_factory=dict)

    def __post_init__(self):
        """Call the setter for initial validation of the passed value."""
        self.db_type = self.initial_db_type
        # Remove the temporary initial_db_type attribute if desired
        del self.initial_db_type

    @property
    def db_type(self) -> ValidDbTypes:
        """The public property getter, returning the validated internal value."""
        # Returns the value from the internal backing field
        return self._db_type

    @db_type.setter
    def db_type(self, value: ValidDbTypes) -> None:
        """The public property setter with validation."""
        # Use self.files here (assuming they are defined as class/instance attributes)
        if value not in self.files.keys():
            raise ValueError(f"Invalid db_type: '{value}'")
        # Store the validated value in the internal backing field
        self._db_type = value

    # --- Methods ---
    def add_to_db(
        self, db_i: Union[Item, Entity, PurchaseOrder, None] = None, id: int = 0
    ) -> None:
        """Adds item to database. If db_i is None, prompts user for data."""

        # 1. Determine ID
        if id == 0:
            id = self.max_id()

        # 2. Get data if not provided (db_i is None)
        if db_i is None:
            # db_i_creator returns Optional[Tuple[data, ent_type]]
            result: Union[Tuple[Dict[str, Any], str], None] = db_i_creator(
                self.db_type, id
            )

            if result:
                data, ent_type = result
                # 3. Create object instance
                # The type checker is happy because self.db_class_type returns a Type
                db_i = self.db_class_type(ent_type)(**data)
            else:
                print("======\nInterrupted by user\n=======\n")
                return None

        # 4. Store in database
        # Ensure db_i is not None before storing (needed for type checking if logic were different)
        if db_i is not None:
            self.db[id] = db_i

    def max_id(self) -> int:
        """Returns the next available ID."""
        try:
            # Check if dict keys are empty; if so, max() raises ValueError
            if not self.db:
                return 1
            return max(self.db.keys()) + 1
        except ValueError:
            # Should be caught by 'if not self.db', but kept as a safeguard
            return 1

    def get_db_i_att(self, db_i_att_name: str) -> List[Any]:
        """Return a list of used values for given attribute name."""
        return [
            getattr(db_item, db_i_att_name)
            for db_item in self.db.values()
            if db_item is not None
        ]

    def db_class_type(self, ent_type: Union[str, int] = 0) -> DbClassType:
        """Returns the appropriate class type (e.g., Item, LegalEntity) based on db_type or ent_type."""
        key = ent_type if isinstance(ent_type, str) else self.db_type

        cls = self.class_map.get(key)
        if cls is None:
            raise ValueError(f"Class type not found for key: {key}")
        return cls

    def store_db(self) -> None:
        """Store the database in a file"""
        file_name = self.files.get(self.db_type, "")
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
                        if db_i is not None:
                            writer.writerow(db_i.serialize())
        except Exception as e:
            print(f"Exception {e} occurred!")
            return None
        print("Database stored in file.\n")

    def load_db(self) -> None:
        """Load the database from a file."""
        file_name = self.files.get(self.db_type)
        if file_name is None:
            return None  # Should not happen

        file_format = file_name.split(".")[-1].upper()

        if file_format not in ["JSON", "CSV"]:
            print(f"File format '{file_format}' not supported!")
            return None

        try:
            with open(file_name, "r", encoding="utf-8") as f:
                data: Union[Dict[str, Any], List[Dict[str, Any]]]

                items_to_load = []

                if file_format == "JSON":
                    data = json.load(f)
                    if isinstance(data, Dict):
                        # JSON loads data as a dictionary of strings, so we iterate over values
                        items_to_load = data.values()
                    elif isinstance(data, List):
                        items_to_load = data

                elif file_format == "CSV":
                    reader = csv.DictReader(f)
                    # CSV reader is an iterable of dictionaries
                    items_to_load = list(reader)

                for value in items_to_load:
                    # 'parse' handles type conversion from strings to native types
                    # id is int, data is Dict[str, Any], ent_type is str or int
                    result: Union[Tuple[int, Dict[str, Any], Union[str, int]], None] = (
                        parse(value, self.db_type)
                    )

                    if result is None:
                        continue  # Skip invalid rows/items

                    id, item_data, ent_type = result

                    # Create object instance
                    DbClass = self.db_class_type(ent_type)
                    db_i = DbClass(**item_data)
                    self.db[id] = db_i

        except FileNotFoundError:
            print(f"File not found: {file_name}. Starting with empty database.")
            return None
        except Exception as e:
            print(f"Exception {e} occurred during loading! Exiting.")
            # Use sys.stderr for error messages if appropriate
            sys.exit(1)

        print(f"Database loaded from file {file_name}")
