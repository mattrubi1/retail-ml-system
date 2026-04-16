import requests
import urllib.parse
import re
import time

HEADERS = {"User-Agent": "Mozilla/5.0"}

SEARCH_TERMS = [
    "drill",
    "impact driver",
    "circular saw",
    "chainsaw",
    "wet dry vac",
    "tool set",
    "grinder",
    "leaf blower",
    "table saw",
    "sander"
]


def extract_product_urls(text):

    matches = re.findall(r"https://www\.homedepot\.com/p/[^\s\"']+", text)

    cleaned = []
    for m in matches:
        url = m.split("?")[0]
        if url not in cleaned:
            cleaned.append(url)

    return cleaned


def fetch_products():

    all_products = []

    for term in SEARCH_TERMS:

        try:
            query = urllib.parse.quote(term)
            url = f"https://www.homedepot.com/s/{query}"

            print(f"Searching: {term}")

            r = requests.get(url, headers=HEADERS, timeout=10)

            if r.status_code != 200:
                print("Blocked:", r.status_code)
                continue

            urls = extract_product_urls(r.text)

            for u in urls[:25]:

                name = u.split("/")[-1].replace("-", " ")

                all_products.append({
                    "name": name.title(),
                    "url": u.split("?")[0]
                })

            time.sleep(1)

        except Exception as e:
            print("ERROR:", e)

    # dedupe
    unique = {p["url"]: p for p in all_products}

    final = list(unique.values())

    print("TOTAL PRODUCTS:", len(final))

    return final
