import string

from typing import Dict, Union, Any
from datetime import date

from validator_collection import validators

from global_data import VALID_ITEMS_IDS_NAMES


LETTERS = {ord(d): str(i) for i, d in enumerate(string.digits + string.ascii_uppercase)}


def _number_iban(iban: str) -> str:
    return (iban[4:] + iban[:4]).translate(LETTERS)


def generate_iban_check_digits(iban: str) -> str:
    number_iban = _number_iban(iban[:2] + "00" + iban[4:])
    return "{:0>2}".format(98 - (int(number_iban) % 97))


def valid_iban(iban: str) -> bool:
    return int(_number_iban(iban)) % 97 == 1


def iban_is_valid(answers: Any = 0, current: str = "None") -> bool:
    if current == "None":
        return False
    iban = current.strip()
    iban = iban.replace(" ", "")
    if generate_iban_check_digits(iban) == iban[2:4] and valid_iban(iban):
        return True
    else:
        return False


def valid_number(answers: Any = 0, current: str = "") -> bool:
    try:
        if current == "":
            print("Value can't be empty.")
            return False
        if float(current) > 0:
            return True
    except ValueError:
        print("\nPlease provide valid number (float or int greater then 0).")
    return False


def valid_mail(answers: Any = 0, current: Union[str, int] = 0) -> bool:
    try:
        validators.email(current)
    except Exception as e:
        print(e)
        return False
    return True


def valid_date(answers: Any = 0, current: Union[str, int] = 0) -> bool:
    try:
        date.fromisoformat(str(current))
    except Exception as e:
        print(f"Error {e}")
        return False
    return True


def not_empty(_: Any, x: str) -> bool:
    try:
        return x.strip() != ""
    except AttributeError:
        print("\nMust be a string")
    return False


def validate_if_in_VALID_ITEMS_IDS_NAMES(answers: Any = 0, current: Union[str, int] = 0) -> bool:
    try:
        return int(current) in VALID_ITEMS_IDS_NAMES
    except Exception as e:
        # print("\n", e)
        return False


if __name__ == "__main__":
    print("--- IBAN Test ---")
    iban = "RO13 RZBR 0000 0600 0713 4800"
    if iban_is_valid(current=iban):
        print("IBAN validation ok!\n")
    else:
        print("IBAN validation not ok!\n")

    print("--- E-mail Test ---")
    print(
        f'Input "someString" is valid (false): {valid_mail("some", current="someString")}'
    )
    print(
        f'Input "some@email.com" is valid (true): {valid_mail(current="some@email.com")}'
    )

    print("--- Number Test ---")
    print(f'Input "34,3" is valid (false): {valid_number(current="34,3")}')
    print(f'Input "0.0" is valid (false): {valid_number(current="0.0")}')
    print(f'Input "-10" is valid (false): {valid_number(current="-10")}')
    print(f'Input "text" is valid (false): {valid_number(current="text")}\n')
    print(f'Input "0.1" is valid(valid): {valid_number(current="0.1")}')
    print(f'Input "1" is valid(valid): {valid_number(current="1")}')

    print("--- Not Empty Test ---")
    print(f'Input " " is valid (false): {not_empty("some", " ")}')
    print(f'Input "" is valid (false): {not_empty("some", "")}')
    print(f"Input 123 is valid (false)): {not_empty('some', 123)}")  # type: ignore
    print(f'Input "abcd" is valid (valid): {not_empty("some", "abcd")}')
    print(f'Input "123" is valid (valid): {not_empty("some", "123")}')
