from dataclasses import dataclass, field
from typing import ClassVar, List, Dict, Tuple, Union, Any
from datetime import date
from global_data import VALID_ENTITIES, VALID_ITEMS_IDS_NAMES
from ui_prompts import invoice


@dataclass
class PurchaseOrder:
    _po_id: int
    _order_date: date
    _customer_id: int
    _invoice_issue_date: Union[date, int] = field(default=0)
    _purchased_items: List[Dict[str, int]] = field(default_factory=list)
    _invoice_id: int = field(default=1)
    _seller_id: int = field(default=1)

    maturity: int = field(default=0)

    VALID_ENTITIES: ClassVar[Dict[int, Any]] = VALID_ENTITIES
    VALID_ITEMS_IDS_NAMES: ClassVar[Dict[int, Any]] = VALID_ITEMS_IDS_NAMES

    # --- DATACLASS LIFECYCLE ---
    def __post_init__(self):
        """Called after __init__ to run setters for validation."""
        # Note: Dataclasses call properties automatically. This is a safeguard
        # if the data needs specific post-processing or if the properties
        # were bypassed during initialization (which they shouldn't be here).
        pass

    @classmethod
    def header(cls) -> List[str]:
        return list(PurchaseOrder.__annotations__.keys())

    def serialize(self) -> dict:
        """Returns a dict ready for JSON/CSV storage."""
        # Access internal fields directly, but use helper methods/logic for dates
        issue_date_value = (
            self.invoice_issue_date
        )  # Use the property to get the date or 0

        print("starting serialize")
        print("order date:", type(self._order_date))
        print("issue date:", type(issue_date_value))

        serialized = {
            "_po_id": self._po_id,
            "order_date": self.order_date.isoformat(),
            "customer_id": self.customer_id,
            "seller_id": self.seller_id,
            "purchased_items": self.purchased_items,
            "_invoice_id": self._invoice_id,
            # Serialize the date only if it's a date object
            "invoice_issue_date": 0
            if issue_date_value == 0
            else issue_date_value.isoformat(),
            "maturity": self.maturity,
        }
        print("serialize:", serialized)
        return serialized

    # --- PROPERTIES AND VALIDATION ---
    @property
    def order_date(self) -> date:
        return date.fromisoformat(str(self._order_date))

    @order_date.setter
    def order_date(self, value: Union[date, str]) -> None:
        """Handles date object or ISO string input."""
        if isinstance(value, str):
            self._order_date = date.fromisoformat(value)
        elif isinstance(value, date):
            self._order_date = value
        else:
            raise TypeError("Order date must be a date object or ISO string.")

    @property
    def invoice_issue_date(self) -> date:
        return date.fromisoformat(str(self._invoice_issue_date))

    @invoice_issue_date.setter
    def invoice_issue_date(self, value: Union[date, str, int]) -> None:
        """Allows setting a date object, an ISO string, or 0."""
        if value == 0:
            self._invoice_issue_date = 0
        elif isinstance(value, str):
            self._invoice_issue_date = date.fromisoformat(value)
        elif isinstance(value, date):
            self._invoice_issue_date = value
        else:
            raise TypeError(
                "Invoice issue date must be 0, a date object, or an ISO string."
            )

    @property
    def customer_id(self) -> int:
        return self._customer_id

    @customer_id.setter
    def customer_id(self, value: int) -> None:
        if int(value) not in list(VALID_ENTITIES.keys()):
            raise ValueError("Invalid buyer ID")
        self._customer_id = int(value)

    @property
    def seller_id(self) -> int:
        return self._seller_id

    @seller_id.setter
    def seller_id(self, value: int) -> None:
        if value not in list(VALID_ENTITIES.keys()):
            raise ValueError("Invalid seller ID")
        self._seller_id = int(value)

    @property
    def purchased_items(self) -> List[Dict[str, int]]:
        return self._purchased_items

    @purchased_items.setter
    def purchased_items(self, value: List[Dict[str, int]]) -> None:
        for item in value:
            if item["item_id"] not in VALID_ITEMS_IDS_NAMES:
                raise ValueError("Invalid item ID")
        self._purchased_items = value

    @property
    def invoice_id(self) -> int:
        return self._invoice_id

    @invoice_id.setter
    def invoice_id(self, value: int) -> None:
        self._invoice_id = int(value)

    # --- OTHER METHODS ---

    def create_invoice(self, invoice_id: int):
        if self._invoice_id == 0:
            data: Dict[str, Any] = invoice()

            self._invoice_id = invoice_id  # Calls invoice_id.setter

            # The setter will handle the type conversion from data dict
            self.invoice_issue_date = data["invoice_issue_date"]
            self.maturity = data["maturity"]
        else:
            print("\nInvoice already exists\n")
            raise Exception("Invoice already created for this PO.")

    @staticmethod
    def get_header() -> List[Tuple]:
        """Returns a user-friendly list of column names for reports/CSV."""
        header = [
            (
                "PO no.",
                "Order date",
                "Customer no.",
                "Customer name",
                "Seller no.",
                "Seller name",
                "Invoice no.",
                "Invoice issue date",
                "Maturity",
            )
        ]
        return header

    def get_i_data(self, entities) -> List[Tuple]:
        if self._invoice_id == 0:
            invoice_id = "Not issued"
            invoice_issue_date = "Not issued"
            maturity = "Not issued"
        else:
            invoice_id = self._invoice_id
            invoice_issue_date = self.invoice_issue_date
            maturity = self.maturity

        line: Tuple = (
            self._po_id,
            self.order_date.isoformat(),
            self.customer_id,
            entities.db[self.customer_id].get_name(),
            self.seller_id,
            entities.db[self.seller_id].get_name(),
            invoice_id,
            invoice_issue_date,
            maturity,
        )
        return [line]
