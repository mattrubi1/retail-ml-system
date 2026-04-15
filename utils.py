import hashlib


def generate_store_sku(item_name: str, store_id: str):

    raw = f"{store_id}-{item_name}"
    short_hash = hashlib.md5(raw.encode()).hexdigest()[:6].upper()

    return f"{store_id}-{item_name[:5].upper()}-{short_hash}"


def normalize_sku(sku: str):
    return str(sku).upper()
