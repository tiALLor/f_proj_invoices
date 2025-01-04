from dataclasses import dataclass, field, asdict
from typing import List, Dict, Any
from datetime import date
from prompts import db_i_creator, invoice, VAT_CATEGORIES
from prompts import VALID_ENTITIES, VALID_ITEMS_IDS_NAMES
from enum import StrEnum


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

    def get_header(self) -> List:
        header = [
            (
                "Item no",
                "Item name",
                "Units",
                "Price [EUR/U]",
                "Vat cat.",
                "Q-ty[units]",
                "Netto [EUR]",
                "VAT %",
                "VAT[EUR]",
                "Brutto [EUR]",
            )
        ]
        return header

    def get_i_data(self, entities) -> List:
        '''entities are not used in this class, used due to common interface'''
        line = [
            (
                str(self._item_id),
                self.item_name + " " + self.item_decription,
                self.item_unit,
                str(self.price_per_unit),
                self._vat_category,
                "Not specified",
                "-",
                "-",
                "-",
                "-",
            )
        ]
        return line

    def get_item_qdata(self, q_ty: str = 0) -> List:
        """Gets item data for specified quantity"""
        data = {"item_netto": "-", "vat_perc": "-", "item_vat": "-", "item_brutto": "-"}
        if q_ty != 0:
            data = self.item_purchase_data(q_ty)
        line = [
            (
                str(self._item_id),
                self.item_name + " " + self.item_decription,
                self.item_unit,
                str(self.price_per_unit),
                self._vat_category,
                str(q_ty),
                str(data["item_netto"]),
                str(data["vat_perc"]),
                str(data["item_vat"]),
                str(data["item_brutto"]),
            )
        ]
        return line

    def item_purchase_data(self, q_ty: int) -> Dict:
        item_purchase_data = {}
        item_purchase_data["item_netto"] = self.price_per_unit * q_ty
        item_purchase_data["vat_perc"] = VAT_CATEGORIES.get(self.vat_category)
        item_purchase_data["item_vat"] = item_purchase_data["item_netto"] * (
            item_purchase_data["vat_perc"] / 100
        )
        item_purchase_data["item_brutto"] = (
            item_purchase_data["item_netto"] + item_purchase_data["item_vat"]
        )
        return item_purchase_data

    @property
    def price_with_vat(self) -> float:
        vat_perc = VAT_CATEGORIES.get(self.vat_category)
        return self.price_per_unit * (1 + vat_perc / 100)
