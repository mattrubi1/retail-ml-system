import requests
from bs4 import BeautifulSoup
import urllib.parse
import re


HEADERS = {
    "User-Agent": "Mozilla/5.0"
}


def search_duckduckgo(query):

    url = "https://duckduckgo.com/html/"

    params = {
        "q": f"site:homedepot.com {query}"
    }

    try:
        r = requests.get(url, params=params, headers=HEADERS, timeout=10)
        soup = BeautifulSoup(r.text, "html.parser")

        results = []

        for a in soup.select("a.result__a"):

            href = a.get("href")
            title = a.get_text()

            if not href:
                continue

            # STRICT FILTER: only real product pages
            if "homedepot.com" in href and re.search(r"/p/|/b/", href):

                results.append({
                    "title": title,
                    "url": href
                })

        return results

    except Exception as e:
        return []


def clean_url(url):

    # Remove tracking junk
    if not url:
        return None

    url = url.split("?")[0]
    return url


def match_product(item_name: str):

    results = search_duckduckgo(item_name)

    if not results:
        return {
            "title": None,
            "url": None,
            "confidence": 0
        }

    best = results[0]

    return {
        "title": best["title"],
        "url": clean_url(best["url"]),
        "confidence": 0.75 if best["url"] else 0
    }
