import hashlib


def generate_store_sku(item_name: str, store_id: str):

    base = f"{store_id}-{item_name}"
    hash_part = hashlib.md5(base.encode()).hexdigest()[:6].upper()

    return f"{store_id}-{item_name[:6].upper()}-{hash_part}"


def normalize_sku(sku: str):
    return str(sku).upper()
