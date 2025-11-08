from dataclasses import dataclass, field, asdict
from typing import Any, List, Dict, Tuple, Union
from global_data import VAT_CATEGORIES


@dataclass(kw_only=True)
class Item:
    # --- Dataclass Fields (Internal Backing Fields) ---
    _item_id: int
    item_name: str
    item_description: str
    item_unit: str  # pcs, m, m2, m3, sets, liter
    _price_per_unit: float
    _vat_category: str  # food, books, services, general
    _valid: bool = field(default=True)
    _currency: str = field(default="EUR")

    # --- Header Methods ---

    @classmethod
    def header(cls) -> List[str]:
        """Returns the public keys expected for serialization/CSV export."""
        return [
            "_item_id",
            "item_name",
            "item_description",
            "item_unit",
            "price_per_unit",
            "vat_category",
            "_valid",
            "_currency",
        ]

    def serialize(self) -> Dict[str, Any]:
        """Returns a dict ready for JSON/CSV storage, using public names."""
        data = asdict(self)

        data["price_per_unit"] = self.price_per_unit
        data["vat_category"] = self.vat_category

        data.pop("_price_per_unit", None)
        data.pop("_vat_category", None)

        return data

    # --- Properties and Validation (No changes needed here) ---

    @property
    def vat_category(self) -> str:
        return self._vat_category

    @vat_category.setter
    def vat_category(self, value: str) -> None:
        if value not in VAT_CATEGORIES.keys():
            raise ValueError(f"Invalid VAT category: {value}")
        self._vat_category = value

    @property
    def price_per_unit(self) -> float:
        return self._price_per_unit

    @price_per_unit.setter
    def price_per_unit(self, value: Union[float, int]) -> None:
        self._price_per_unit = float(value)

    @staticmethod
    def get_header() -> List[Tuple]:
        """Returns a user-friendly list of column names for reports/CSV."""
        # FIX: Return a flattened list of strings instead of a List[Tuple]
        return [
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

    # --- Calculation Methods (No major changes needed here) ---

    def item_purchase_data(self, q_ty: Union[int, float]) -> Dict[str, float]:
        item_purchase_data: Dict[str, float] = {}
        vat_perc = VAT_CATEGORIES.get(self.vat_category, 0.0)

        item_purchase_data["item_netto"] = self.price_per_unit * q_ty
        item_purchase_data["vat_perc"] = float(vat_perc)

        item_purchase_data["item_vat"] = item_purchase_data["item_netto"] * (
            item_purchase_data["vat_perc"] / 100
        )
        item_purchase_data["item_brutto"] = (
            item_purchase_data["item_netto"] + item_purchase_data["item_vat"]
        )
        return item_purchase_data

    @property
    def price_with_vat(self) -> float:
        vat_perc = VAT_CATEGORIES.get(self.vat_category, 0.0)
        return self.price_per_unit * (1 + vat_perc / 100.0)

    # --- Display Methods (Minor type cleanup) ---

    def get_i_data(self, entities: Any) -> List[Tuple]:
        """Gets basic item data for a general list/report."""
        line: Tuple = (
            str(self._item_id),
            self.item_name + " " + self.item_description,
            self.item_unit,
            str(self.price_per_unit),
            self.vat_category,
            "Not specified",
            "-",
            "-",
            "-",
            "-",
        )
        return [line]

    def get_item_qdata(self, q_ty: Union[int, float, str] = 0) -> List[Tuple]:
        """Gets item data formatted for a specified quantity."""

        try:
            q_ty_num = float(q_ty)
        except (ValueError, TypeError):
            q_ty_num = 0.0

        if q_ty_num > 0:
            data_calc = self.item_purchase_data(q_ty_num)

            netto_str = f"{data_calc['item_netto']:.2f}"
            vat_str = f"{data_calc['item_vat']:.2f}"
            brutto_str = f"{data_calc['item_brutto']:.2f}"
            vat_perc_str = str(data_calc["vat_perc"])
            q_ty_str = str(q_ty_num)
        else:
            netto_str = "-"
            vat_str = "-"
            brutto_str = "-"
            vat_perc_str = "-"
            q_ty_str = str(q_ty)

        line: List[Tuple] = [
            (
                str(self._item_id),
                self.item_name + " " + self.item_description,
                self.item_unit,
                str(self.price_per_unit),
                self.vat_category,
                q_ty_str,
                netto_str,
                vat_perc_str,
                vat_str,
                brutto_str,
            )
        ]
        return line
