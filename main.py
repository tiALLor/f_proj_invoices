from pprint import pprint
from database import IndivEntity, LegalEntity, Item, PurchaseOrder, Database


def main():
    items = Database(db_type="Item")
    # items.load_db()
    items.add_to_db(Item(1, "Screw", "M5x20", "pcs", 0.1, "general"))
    items.add_to_db(Item(2, "Nut", "M5", "pcs", 0.2, "general"))
    items.store_db()
    pprint(items.db)
    print(type(items.db[1]._valid))

    entity = Database(db_type="Entity")
    entity.add_to_db(LegalEntity(
        1, "Aludarių g. 3", "Vilnius", "Lithuania", "LT-LT-01113",
        "study@turingcollege.com", "123456789","LegalEntity",
        "Turing College", "LT47395850", "4739585",
        "RO13 RZBR 0000 0600 0713 4800"))
    entity.add_to_db(IndivEntity(
        2, "Ferenc Liszt 5", "Warsaw", "Poland", "00-000",
        "JognDoe@gmail.com", "123456789", "IndivEntity", "John",
        None, "Doe"))
    entity.store_db()
    # entity.load_db()
    pprint(entity.db)



if __name__ == "__main__":
    main()
