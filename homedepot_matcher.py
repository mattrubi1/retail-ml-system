import requests
from bs4 import BeautifulSoup
import urllib.parse

HEADERS = {
    "User-Agent": "Mozilla/5.0"
}


def search_homedepot(query: str):

    url = "https://www.homedepot.com/s/" + urllib.parse.quote(query)

    try:
        r = requests.get(url, headers=HEADERS, timeout=10)
        soup = BeautifulSoup(r.text, "html.parser")

        products = soup.select("div.product-pod")

        results = []

        for p in products[:5]:

            title_tag = p.select_one("a.product-pod--title__product")
            link_tag = p.select_one("a")

            if not title_tag:
                continue

            title = title_tag.get_text(strip=True)
            link = "https://www.homedepot.com" + link_tag["href"] if link_tag else None

            results.append({
                "title": title,
                "url": link
            })

        return results

    except Exception:
        return []


def match_product(item_name: str):

    results = search_homedepot(item_name)

    if not results:
        return {
            "title": None,
            "url": None,
            "confidence": 0
        }

    best = results[0]

    return {
        "title": best["title"],
        "url": best["url"],
        "confidence": 0.8
    }
