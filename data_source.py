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


def fetch_from_duckduckgo(term):

    try:
        query = urllib.parse.quote(f"site:homedepot.com {term}")
        url = f"https://duckduckgo.com/html/?q={query}"

        r = requests.get(url, headers=HEADERS, timeout=10)
        html = r.text

        matches = re.findall(r"https://www\.homedepot\.com/p/[^\s\"']+", html)

        return [m.split("?")[0] for m in matches[:3]]

    except Exception:
        return []


def fallback_home_depot(term):
    """
    Guaranteed fallback using Home Depot search page
    """

    query = urllib.parse.quote(term)
    return [f"https://www.homedepot.com/s/{query}"]


def fetch_products():

    products = []

    for term in SEARCH_TERMS:

        urls = fetch_from_duckduckgo(term)

        # 🔥 fallback if nothing found
        if not urls:
            print(f"⚠️ Fallback triggered for: {term}")
            urls = fallback_home_depot(term)

        for u in urls:
            products.append({
                "name": term,
                "url": u
            })

    return products
