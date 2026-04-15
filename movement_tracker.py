import pandas as pd

def detect_movement(current, history):

    # find items that changed store
    merged = current.merge(
        history,
        on="sku",
        suffixes=("_new", "_old")
    )

    moved = merged[
        merged["last_store_location_new"] != merged["last_store_location_old"]
    ]

    return moved[[
        "sku",
        "item_name_new",
        "last_store_location_old",
        "last_store_location_new"
    ]]
