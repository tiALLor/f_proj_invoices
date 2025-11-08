from dataclasses import dataclass, asdict
from typing import List, Dict, Any, Literal, Tuple


@dataclass
class Entity:
    _entity_id: int
    street_number: str
    city: str
    country: str
    postal_code: str
    email: str
    phone_no: str
    ent_type: Literal["IndivEntity", "LegalEntity"]

    def get_name(self) -> str: ...

    def serialize(self) -> Dict[str, Any]:
        data = asdict(self)

        # Add 'Empty' placeholders for common optional fields
        data.setdefault("first_name", "Empty")
        data.setdefault("second_name", "Empty")
        data.setdefault("last_name", "Empty")
        data.setdefault("company_name", "Empty")
        data.setdefault("vat_id", "Empty")
        data.setdefault("tax_id", "Empty")
        data.setdefault("bank_account", "Empty")

        return data

    @classmethod
    def header(cls) -> List[str]:
        fields: list[str] = []
        fields.extend(list(Entity.__annotations__.keys()))
        fields.extend(list(IndivEntity.__annotations__.keys()))
        fields.extend(list(LegalEntity.__annotations__.keys()))
        return fields

    def get_address(self) -> list[str]:
        data: list[str] = []
        data.append(self.street_number.capitalize())
        data.append(f"{self.postal_code} {self.city}")
        data.append(self.country)
        data.append(f"e-mail: {self.email}")
        data.append(f"phone:{self.phone_no}" if self.phone_no != "None" else "")
        return data

    @staticmethod
    def get_header() -> List[Tuple]:
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

    def get_i_data(self, entities) -> List[Tuple[Any, ...]]:
        """entities are not used in this class, used due to common interface"""
        serialized_data = self.serialize()

        # The structure should match the order in get_header (or be consistent)
        line = [
            (
                serialized_data["_entity_id"],
                self.get_name(),
                serialized_data["street_number"],
                serialized_data["city"],
                serialized_data["postal_code"],
                serialized_data["country"],
                serialized_data["email"],
                serialized_data["phone_no"],
                serialized_data["ent_type"],
                serialized_data["vat_id"],
                serialized_data["tax_id"],
                serialized_data["bank_account"],
            )
        ]
        # Change the return type to a single tuple, not a set of one tuple.
        return line


@dataclass
class IndivEntity(Entity):
    first_name: str
    second_name: str
    last_name: str

    def get_name(self) -> str:
        name_parts = [self.first_name]
        if self.second_name and self.second_name != "Empty":
            name_parts.append(self.second_name)
        name_parts.append(self.last_name)
        name = " ".join(name_parts)
        return name.upper()


@dataclass
class LegalEntity(Entity):
    company_name: str
    vat_id: str
    tax_id: str
    bank_account: str

    def get_name(self) -> str:
        data: str = f"{self.company_name}"
        return data

    def get_company_data(self) -> List[str]:
        data: List[str] = []
        data.append(f"VAT ID: {self.vat_id}")
        data.append(f"TAX ID: {self.tax_id}")
        data.append(f"Bank details: {self.bank_account}")
        return data
