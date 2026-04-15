import requests
from bs4 import BeautifulSoup
import urllib.parse


HEADERS = {
    "User-Agent": "Mozilla/5.0"
}


def search_web(query):

    url = f"https://duckduckgo.com/html/?q=site:homedepot.com+{urllib.parse.quote(query)}"

    try:
        r = requests.get(url, headers=HEADERS, timeout=10)
        soup = BeautifulSoup(r.text, "html.parser")

        results = []

        for a in soup.select("a.result__a")[:5]:

            href = a.get("href")
            title = a.get_text()

            if href and "homedepot.com" in href:

                results.append({
                    "title": title,
                    "url": href
                })

        return results

    except Exception:
        return []


def match_product(item_name: str):

    results = search_web(item_name)

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
        "confidence": 0.85
    }
