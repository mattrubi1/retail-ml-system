import hashlib


def generate_store_sku(item_name: str, store_id: str):
    """
    Creates a stable SKU based on store + item name
    Same input ALWAYS produces same SKU
    """

    key = f"{store_id}-{item_name}"

    hash_obj = hashlib.md5(key.encode())
    hash_hex = hash_obj.hexdigest()

    return f"SKU-{hash_hex[:3]}-{hash_hex[3:6]}-{hash_hex[6:9]}"


def normalize_sku(sku: str):
    return str(sku).upper()
