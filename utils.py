import numpy as np

# =========================
# GENERATE SKU (XXXX-XXX-XXX)
# =========================
def generate_sku():

    raw = str(np.random.randint(1000000000, 9999999999))

    return f"{raw[:4]}-{raw[4:7]}-{raw[7:10]}"


# =========================
# NORMALIZE ANY SKU INPUT
# =========================
def normalize_sku(value):

    if value is None:
        return generate_sku()

    value = str(value)

    digits = "".join(filter(str.isdigit, value))

    digits = digits.zfill(10)

    return f"{digits[:4]}-{digits[4:7]}-{digits[7:10]}"
