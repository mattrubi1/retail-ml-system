import requests
import re
import urllib.parse

HEADERS = {"User-Agent": "Mozilla/5.0"}


SEARCH_TERMS = [
    "Milwaukee drill",
    "DeWalt impact driver",
    "Ryobi chainsaw",
    "Rigid wet dry vac",
    "Makita grinder",
    "Husky tool set"
]


def fetch_products():

    products = []

    for term in SEARCH_TERMS:

        try:
            query = urllib.parse.quote(f"site:homedepot.com {term}")
            url = f"https://duckduckgo.com/html/?q={query}"

            r = requests.get(url, headers=HEADERS, timeout=10)
            html = r.text

            matches = re.findall(r"https://www\.homedepot\.com/p/[^\s\"']+", html)

            for m in matches[:3]:

                clean_url = m.split("?")[0]

                products.append({
                    "name": term,
                    "url": clean_url
                })

        except Exception:
            continue

    return products
