from typing import Dict, List

# Define types for the global lookup dictionaries
VALID_ENTITIES: Dict[int, str] = {}
"""Stores valid entity_ids: name from the database entities.db for validation"""

VALID_ITEMS_IDS_NAMES: Dict[int, str] = {}
"""Stores valid item_ids: names from the database items.db for validation"""

ITEM_UNITS: List[str] = ["pcs", "m", "m2", "m3", "sets", "liters"]

VAT_CATEGORIES: Dict[str, int] = {
    """ VAT category and VAT value in % """
    "food": 5,
    "books": 10,
    "services": 21,
    "general": 21,
    "accommodations": 10,
}
