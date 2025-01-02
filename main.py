from pprint import pprint
from database import IndivEntity, LegalEntity, Item, PurchaseOrder, Database
from prompts import VALID_ENTITIES, VALID_ITEMS_IDS_NAMES


def update_valid_lists():
        for entity in entities.db.values():
            if isinstance(entity, IndivEntity):
                VALID_ENTITIES.update({entity._entity_id: entity.last_name})
            elif isinstance(entity, LegalEntity):
                VALID_ENTITIES.update({entity._entity_id: entity.company_name})
            else:
                 raise ValueError("Unknown entity type")
        for item in items.db.values():
            VALID_ITEMS_IDS_NAMES.update({item._item_id: item.item_name})
            
             
def main():
    global items
    items = Database(db_type="Item")

    items.load_db()
    # items.add_to_db(Item(1, "Screw", "M5x20", "pcs", 0.1, "general"))
    # items.add_to_db(Item(2, "Nut", "M5", "pcs", 0.2, "general"))
    # items.store_db()
    # items.add_to_db()               # debug 
    pprint(items.db)
    print(type(items.db[1]._valid))

    global entities
    entities = Database(db_type="Entity")
    entities.add_to_db(LegalEntity(
        1, "Aludarių g. 3", "Vilnius", "Lithuania", "LT-LT-01113",
        "study@turingcollege.com", "123456789",
        "Turing College", "LT47395850", "4739585",
        "RO13 RZBR 0000 0600 0713 4800"))
    entities.add_to_db(IndivEntity(
        2, "Ferenc Liszt 5", "Warsaw", "Poland", "00-000",
        "JognDoe@gmail.com", "123456789", "John",
        None, "Doe"))
    entities.store_db()
    # entity.load_db()
    # entity.add_to_db()          # debug

    pprint(entities.db)

    
    # fulling the lists with valid entities and items
    update_valid_lists()
    # VALID_ENTITIES.extend(entities.db.keys())
    # VALID_ITEMS_IDS_NAMES.update({item._item_id: item.item_name for item in items.db.values()})
    # VALID_ITEMS_IDS.extend(items.db.keys())
    # VALID_ITEM_NAMES.extend([item.item_name for item in items.db.values()])
    print(VALID_ENTITIES)   # debug
    print(VALID_ITEMS_IDS_NAMES)  # debug
    print(type(VALID_ITEMS_IDS_NAMES.keys()))
    print(list(VALID_ITEMS_IDS_NAMES.keys()))  # debug
    # print(VALID_ITEM_NAMES) # debug

    global purchase_orders
    purchase_orders = Database(db_type="PurchaseOrder")
    purchase_orders.load_db()
    # purchase_orders.add_to_db(PurchaseOrder(
    #     1, "2024-12-31", 2, 1,
    #     [{"item_id": 1,"item_q_ty": 20}, {"item_id": 2,"item_q_ty": 10}],
    # ))
    # purchase_orders.store_db()
    purchase_orders.add_to_db()
    pprint(purchase_orders.db)



if __name__ == "__main__":
    main()
