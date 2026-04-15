def generate_store_sku(item_name: str, store_id: str):
    return f"{store_id}-{item_name[:5].upper()}-{abs(hash(item_name)) % 9999}"


def normalize_sku(sku: str):
    return str(sku).upper()
