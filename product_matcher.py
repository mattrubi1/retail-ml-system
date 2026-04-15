import requests
from bs4 import BeautifulSoup
import urllib.parse
import re

HEADERS = {
    "User-Agent": "Mozilla/5.0"
}


def _extract_homedepot_urls(html):
    soup = BeautifulSoup(html, "html.parser")

    results = []

    for a in soup.select("a.result__a"):
        href = a.get("href")
        title = a.get_text(strip=True)

        if not href:
            continue

        # Keep only real product/browse pages
        if "homedepot.com" in href and ("/p/" in href or "/b/" in href):
            results.append({
                "title": title,
                "url": href.split("?")[0]
            })

    return results


def search_homedepot(query):
    url = "https://duckduckgo.com/html/"
    params = {"q": f"site:homedepot.com {query}"}

    try:
        r = requests.get(url, params=params, headers=HEADERS, timeout=10)
        return _extract_homedepot_urls(r.text)
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

    confidence = 0.8 if "/p/" in best["url"] else 0.5

    return {
        "title": best["title"],
        "url": best["url"],
        "confidence": confidence
    }
