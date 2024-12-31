import string
from validator_collection import validators, errors


LETTERS = {ord(d): str(i) for i, d in enumerate(string.digits + string.ascii_uppercase)}


def _number_iban(iban):
    return (iban[4:] + iban[:4]).translate(LETTERS)


def generate_iban_check_digits(iban):
    number_iban = _number_iban(iban[:2] + "00" + iban[4:])
    return "{:0>2}".format(98 - (int(number_iban) % 97))


def valid_iban(iban):
    return int(_number_iban(iban)) % 97 == 1


def iban_is_valid(answers=0, current=0):
    if current == "None":
        return True
    iban = current.strip()
    iban = iban.replace(" ", "")
    if generate_iban_check_digits(iban) == iban[2:4] and valid_iban(iban):
        return True
    else:
        return False


def valid_number(answers=0, current=0):
    try:
        if current == "":
            print("Value can't be empty.")
            return False
        if float(current) > 0:
            return True
    except ValueError:
        print("\nPlease provide valid number (float or int greter then 0).")
    return False


def valid_mail(answers=0, current=0):
    try:
        validators.email(current)
    except Exception as e:
        print(e)
        return False
    return True


if __name__ == "__main__":
    iban = "RO13 RZBR 0000 0600 0713 4800"
    if iban_is_valid(current=iban):
        print("IBAN ok!\n")
    else:
        print("IBAN not ok!\n")

    print(valid_number(current="34,3"), "\n")
