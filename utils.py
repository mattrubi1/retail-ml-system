import hashlib


def generate_store_sku(item_name: str, store_id: str):

    key = f"{store_id}-{item_name}"
    hash_hex = hashlib.md5(key.encode()).hexdigest()

    return f"SKU-{hash_hex[:3]}-{hash_hex[3:6]}-{hash_hex[6:9]}"


def normalize_sku(sku: str):
    return str(sku).upper()
