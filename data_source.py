import requests
import re
import urllib.parse
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
    "leaf blower"
]


def extract_products(html):

    matches = re.findall(r"https://www\.homedepot\.com/p/[^\s\"']+", html)

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

            # IMPORTANT: use REAL search endpoint (not category pages)
            url = f"https://www.homedepot.com/s/{query}"

            print(f"Searching: {term}")

            r = requests.get(url, headers=HEADERS, timeout=10)

            if r.status_code != 200:
                print("Blocked:", r.status_code)
                continue

            products = extract_products(r.text)

            if not products:
                print(f"No products found for: {term}")

            for p in products[:20]:

                name = p.split("/")[-1].replace("-", " ")

                all_products.append({
                    "name": name.title(),
                    "url": p.split("?")[0]
                })

            time.sleep(1)

        except Exception as e:
            print("ERROR:", e)

    # deduplicate
    unique = {p["url"]: p for p in all_products}

    final = list(unique.values())

    print("TOTAL PRODUCTS:", len(final))

    return final
