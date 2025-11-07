from datetime import date
from typing import NotRequired, TypedDict, Callable, Literal, List, Union, Tuple
from .validators import iban_is_valid, valid_number, valid_mail, valid_date, not_empty
from global_data import VALID_ITEMS_IDS_NAMES, ITEM_UNITS, VAT_CATEGORIES


class QuestionConfirm(TypedDict):
    type: Literal["confirm"]
    message: str
    default: NotRequired[bool]


class QuestionText(TypedDict):
    type: Literal["text"]
    name: str
    message: str
    validate: NotRequired[Callable[[object, str], bool]]  # matches your not_empty(_, x)
    default: NotRequired[str]


class QuestionList(TypedDict):
    type: Literal["list"]
    name: str
    message: str
    choices: Union[List[str], List[Tuple[str, str]]]
    default: NotRequired[str]
    carousel: NotRequired[bool]


InputQuestionData = Union[QuestionConfirm, QuestionText, QuestionList]

confirm_question_data: List[InputQuestionData] = [
    {"type": "confirm", "message": "Confirm the action?", "default": True},
]

entity_type_question_data: List[InputQuestionData] = [
    {
        "type": "list",
        "name": "entity_type",
        "message": "Which entity type are you adding?",
        "choices": ["IndivEntity", "LegalEntity"],
        "carousel": True,
    },
]

# Shared Entity Fields
entity_questions_data: List[InputQuestionData] = [
    {
        "type": "text",
        "name": "street_number",
        "message": "Street and house number",
        "validate": not_empty,
    },
    {
        "type": "text",
        "name": "city",
        "message": "City",
        "validate": not_empty,
    },
    {
        "type": "text",
        "name": "country",
        "message": "Country",
        "validate": not_empty,
    },
    {
        "type": "text",
        "name": "postal_code",
        "message": 'Postal code"',
        "validate": not_empty,
    },
    {
        "type": "text",
        "name": "phone_no",
        "message": "Phone number",
        "validate": not_empty,
        "default": "None",
    },
    {
        "type": "text",
        "name": "email",
        "message": "E-mail",
        "validate": valid_mail,
    },
]

# IndivEntity Fields
indiv_entity_question_data: List[InputQuestionData] = [
    {
        "type": "text",
        "name": "first_name",
        "message": "First name",
        "validate": not_empty,
    },
    {
        "type": "text",
        "name": "second_name",
        "message": "Middle name (optional)",
        "validate": not_empty,
        "default": "None",
    },
    {
        "type": "text",
        "name": "last_name",
        "message": "Last name",
        "validate": not_empty,
    },
]

# LegalEntity Fields
legal_entity_question_data: List[InputQuestionData] = [
    {
        "type": "text",
        "name": "company_name",
        "message": "Company's name",
        "validate": not_empty,
    },
    {
        "type": "text",
        "name": "vat_id",
        "message": "VAT number",
        "validate": not_empty,
    },
    {
        "type": "text",
        "name": "tax_id",
        "message": "TAX number",
        "validate": not_empty,
    },
    {
        "type": "text",
        "name": "tax_id",
        "message": "TAX number",
        "validate": not_empty,
    },
    {
        "type": "text",
        "name": "bank_account",
        "message": "Bank account number",
        "validate": iban_is_valid,
        "default": "None",
    },
]

# Item Fields
item_question_data: List[InputQuestionData] = [
    {
        "type": "text",
        "name": "item_name",
        "message": "Item name",
        "validate": not_empty,
    },
    {
        "type": "text",
        "name": "item_description",
        "message": "Item description (optional)",
        "validate": not_empty,
        "default": "None",
    },
    {
        "type": "list",
        "name": "item_unit",
        "message": "Item unit",
        "choices": ITEM_UNITS,
        "carousel": True,
    },
    {
        "type": "text",
        "name": "price_per_unit",
        "message": "Price per unit [EUR] (without VAT)",
        "validate": valid_number,
        "default": "None",
    },
    {
        "type": "list",
        "name": "vat_category",
        "message": "VAT category",
        "choices": list(VAT_CATEGORIES.keys()),
        "default": "general",
        "carousel": True,
    },
]


# Purchase Order Fields
purchase_order_question_data: List[InputQuestionData] = [
    {
        "type": "text",
        "name": "item_ID",
        "message": "Item ID to be purchased",
        "validate": lambda _, x: int(x) in VALID_ITEMS_IDS_NAMES,
    },
]

purchase_item_question_data: List[InputQuestionData] = [
    {
        "type": "text",
        "name": "item_ID",
        "message": "Item ID to be purchased",
        "validate": lambda _, x: int(x) in VALID_ITEMS_IDS_NAMES,
    },
    {
        "type": "text",
        "name": "q_ty",
        "message": "Quantity of item units",
        "validate": valid_number,
    },
]

invoice_question_data: List[InputQuestionData] = [
    {
        "type": "text",
        "name": "invoice_issue_date",
        "message": "The date of invoice was issued(YYYY-MM-DD)",
        "validate": valid_date,
        "default": date.today().isoformat(),
    },
    {
        "type": "text",
        "name": "maturity",
        "message": "Maturity of the invoice [days] (from payment terms)",
        "validate": valid_number,
        "default": "14",
    },
]

# ui Fields
get_operation_question_data: List[InputQuestionData] = [
    {
        "type": "list",
        "name": "operation",
        "message": "Please choose what you would like to do:",
        "choices": [
            ("1. Add a Customer (Entity)", "1"),
            ("2. Add a Item as product or service", "2"),
            ("3. Create a Purchase Order(PO)", "3"),
            ("4. Invoice: issue and send to the customer", "4"),
            ("5. Show Customers (Entities)", "5"),
            ("6. Show Items (products or services)", "6"),
            ("7. Show Purchase Orders (PO) and Invoices", "7"),
            ("8. Show purchased items in a PO", "8"),
            ("9. Quit (End the program)", "9"),
        ],
        "carousel": True,
    },
]

get_po_number_question_data: List[InputQuestionData] = [
    {
        "type": "text",
        "name": "po_id",
        "message": "Please specify the Purchase Order (PO)",
        "validate": valid_number,
    },
]
