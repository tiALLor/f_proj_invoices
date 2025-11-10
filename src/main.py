from prompts.ui_prompts import get_operation
from main_handlers_and_store import (
    database_initialization,
    # database_debug,
    op_entities,
    op_items,
    op_purchase_orders,
    op_create_invoice,
    op_show_entities,
    op_show_items,
    op_show_purchase_orders,
    op_show_po_items,
    op_exit,
)
# import sys


def primary_screen() -> None:
    """Main loop for handling user operations via a dispatch table."""

    operations = {
        "1": op_entities,
        "2": op_items,
        "3": op_purchase_orders,
        "4": op_create_invoice,
        "5": op_show_entities,
        "6": op_show_items,
        "7": op_show_purchase_orders,
        "8": op_show_po_items,
        "9": op_exit,
    }

    while True:
        operation = get_operation()
        action = operations.get(operation)
        if action:
            action()
        else:
            print("Unknown operation. Please select a valid number from the menu.")
            # sys.exit("Unknown operation.")


def main():
    database_initialization()
    # database_debug()      # debug
    primary_screen()


if __name__ == "__main__":
    main()
