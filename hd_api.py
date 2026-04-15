import requests

def get_product_data(sku):

    url = f"https://www.homedepot.com/p/{sku}"

    headers = {
        "User-Agent": "Mozilla/5.0"
    }

    try:
        r = requests.get(url, headers=headers, timeout=10)
        text = r.text

        # VERY SIMPLE PARSING (works surprisingly well)
        name = "Unknown Item"
        price = 0.0
        image = ""

        if '"productLabel":"' in text:
            name = text.split('"productLabel":"')[1].split('"')[0]

        if '"value":' in text:
            price = float(text.split('"value":')[1].split(",")[0])

        if '"image":"' in text:
            image = text.split('"image":"')[1].split('"')[0]

        return {
            "item_name": name,
            "price": price,
            "image": image
        }

    except:
        return {
            "item_name": "Error fetching",
            "price": 0,
            "image": ""
        }
