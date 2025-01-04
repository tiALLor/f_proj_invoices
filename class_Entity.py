from dataclasses import dataclass, field, asdict
from typing import List, Dict, Any
from datetime import date
from prompts import db_i_creator, invoice, VAT_CATEGORIES
from prompts import VALID_ENTITIES, VALID_ITEMS_IDS_NAMES
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

    def get_name(self): ...

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
            "first_name": self.first_name if hasattr(self, "first_name") else "Empty",
            "second_name": self.second_name
            if hasattr(self, "second_name")
            else "Empty",
            "last_name": self.last_name if hasattr(self, "last_name") else "Empty",
            "company_name": self.company_name
            if hasattr(self, "company_name")
            else "Empty",
            "vat_id": self.vat_id if hasattr(self, "vat_id") else "Empty",
            "tax_id": self.tax_id if hasattr(self, "tax_id") else "Empty",
            "bank_account": self.bank_account
            if hasattr(self, "bank_account")
            else "Empty",
        }
        return serialized

    @classmethod
    def header(cls) -> List[str]:
        fields = []
        fields.extend(list(Entity.__annotations__.keys()))
        fields.extend(list(IndivEntity.__annotations__.keys()))
        fields.extend(list(LegalEntity.__annotations__.keys()))
        return fields

    def get_adress(self) -> str:
        data = []
        data.append(self.street_number.capitalize())
        data.append(f"{self.postal_code} {self.city}")
        data.append(self.country)
        data.append(f"e-mail: {self.email}")
        data.append(f"phone:{self.phone_no}" if self.phone_no != "None" else None)
        return data

    def get_header(self) -> List:
        header = [
            (
                "Entity no.",
                "Name",
                "Street and number",
                "City",
                "Postal code",
                "Country",
                "E-mail",
                "Phone number",
                "Entity type",
                "VAT no.",
                "TAX no.",
                "Bank account",
            )
        ]
        return header

    def get_i_data(self, entities) -> List:
        '''entities are not used in this class, used due to common interface'''
        line = {
            (
                self._entity_id,
                ",".join(str(element) for element in self.get_name()),
                self.street_number,
                self.city,
                self.postal_code,
                self.country,
                self.email,
                self.phone_no,
                self.ent_type,
                self.vat_id if hasattr(self, "vat_id") else "Empty",
                self.tax_id if hasattr(self, "tax_id") else "Empty",
                self.bank_account if hasattr(self, "bank_account") else "Empty",
            )
        }
        return line


@dataclass
class IndivEntity(Entity):
    first_name: str
    second_name: str
    last_name: str
    ent_type: str = "IndivEntity"

    def get_name(self) -> str:
        data = []
        name = f"{self.first_name} {"" if self.second_name == "None" else f"{self.second_name}"} {self.last_name}"
        data.append(name.upper())
        return data


@dataclass
class LegalEntity(Entity):
    company_name: str
    vat_id: str
    tax_id: str
    bank_account: str
    ent_type: str = "LegalEntity"

    def get_name(self) -> List:
        data = [f"{self.company_name}"]
        return data

    def get_company_data(self) -> List:
        data = []
        data.append(f"VAT ID: {self.vat_id}")
        data.append(f"TAX ID: {self.tax_id}")
        data.append(f"Bank details: {self.bank_account}")
        return data
