from dataclasses import dataclass, field, asdict
from typing import List, Dict, Any
from datetime import date
from prompts import db_i_creator, invoice, VAT_CATEGORIES
from prompts import VALID_ENTITIES, VALID_ITEMS_IDS_NAMES
from enum import StrEnum


@dataclass
class PurchaseOrder:
    _po_id: int
    order_date: date
    customer_id: int
    seller_id: int = field(default=1)
    purchased_items: List[Dict[str, int]] = field(default_factory=list)
    _invoice_id: int = field(default=0)
    invoice_issue_date: date = field(default=0)
    maturity: int = field(default=0)

    @classmethod
    def header(cls) -> List[str]:
        return list(PurchaseOrder.__annotations__.keys())

    def serialize(self) -> dict:
        serialized = {
            "_po_id": self._po_id,
            "order_date": date.isoformat(self.order_date),
            "customer_id": self.customer_id,
            "seller_id": self.seller_id,
            "purchased_items": self.purchased_items,
            "_invoice_id": self._invoice_id,
            "invoice_issue_date": 0
            if self.invoice_issue_date == 0
            else date.isoformat(self.invoice_issue_date),
            "maturity": self.maturity,
        }
        return serialized

    @property
    def order_date(self) -> date:
        return self._order_date

    @order_date.setter
    def order_date(self, value: str) -> None:
        self._order_date = date.fromisoformat(value)

    @property
    def customer_id(self) -> int:
        return self._customer_id

    @customer_id.setter
    def customer_id(self, value: int) -> None:
        if int(value) not in list(VALID_ENTITIES.keys()):
            raise ValueError("Invalid buyer ID")
        self._customer_id = int(value)

    # Currently not used
    # @property
    # def seller_id(self) -> int:
    #     return self._seller_id

    # @seller_id.setter
    # def seller_id(self, value: int) -> None:
    #     if value not in list(VALID_ENTITIES.keys()):
    #         raise ValueError("Invalid seller ID")
    #     self._seller_id = value

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

    # @property
    # def invoice_issue_date(self) -> date:
    #     return self._invoice_issue_date

    # @invoice_issue_date.setter
    # def invoice_issue_date(self, value: str) -> None:
    #     self._invoice_issue_date = date.fromisoformat(value)

    def create_invoice(self, invoice_id):
        if self._invoice_id == 0:
            data = invoice()
            self._invoice_id = invoice_id
            self.invoice_issue_date = data["invoice_issue_date"]
            self.maturity = data["maturity"]
        else:
            print("\nInvoice already exists\n")
            raise Exception()

    def get_header(self) -> List:
        header = [
            (
                "PO no.",
                "Order date",
                "Customer no.",
                "Customer name",
                "Seller no.",
                "Seller name",
                "Invoice no.",
                "Invoce issue date",
                "Maturity",
            )
        ]
        return header

    def get_i_data(self, entities) -> List:
        if self._invoice_id == 0:
            invoice_id = "Not issued"
            invoice_issue_date = "Not issued"
            maturity = "Not issued"
        else:
            invoice_id = self._invoice_id
            invoice_issue_date = self.invoice_issue_date
            maturity = self.maturity

        line = [
            (
                self._po_id,
                date.isoformat(self.order_date),
                self.customer_id,
                entities.db[self.customer_id].get_name(),
                self.seller_id,
                entities.db[self.seller_id].get_name(),
                invoice_id,
                invoice_issue_date,
                maturity,
            )
        ]
        return line
