import requests
import re
import json

HEADERS = {"User-Agent": "Mozilla/5.0"}


def extract_json_blob(html):
    """
    Pull embedded JSON from Home Depot product page
    """

    match = re.search(r'window\.__APOLLO_STATE__\s*=\s*({.*});', html)

    if match:
        return match.group(1)

    return None


def parse_price(data):

    try:
        parsed = json.loads(data)

        # search for price fields dynamically
        for key in parsed:
            val = parsed[key]

            if isinstance(val, dict):

                if "price" in val:
                    price_block = val.get("price")

                    if isinstance(price_block, dict):

                        if "value" in price_block:
                            return float(price_block["value"])

    except Exception as e:
        print("JSON parse error:", e)

    return None


def fetch_price(url):

    try:
        r = requests.get(url, headers=HEADERS, timeout=10)

        if r.status_code != 200:
            return None

        html = r.text

        json_blob = extract_json_blob(html)

        if not json_blob:
            return None

        price = parse_price(json_blob)

        return price

    except Exception as e:
        print("Price fetch error:", e)
        return None
