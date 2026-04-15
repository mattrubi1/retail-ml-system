def generate_store_sku(item_name: str, store_id: str):

    # REAL SYSTEM: no fake SKU generation
    return f"{store_id}-{item_name}".replace(" ", "-").upper()


def normalize_sku(sku: str):
    return str(sku).upper()
