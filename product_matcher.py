import requests
import re
import urllib.parse

HEADERS = {"User-Agent": "Mozilla/5.0"}


def match_product(item_name: str):
    """
    SAFE matcher:
    - tries to find Home Depot URL
    - always returns structured output
    """

    try:
        query = urllib.parse.quote(f"site:homedepot.com {item_name}")
        url = f"https://duckduckgo.com/html/?q={query}"

        r = requests.get(url, headers=HEADERS, timeout=10)
        html = r.text

        # Extract ANY Home Depot URLs
        urls = re.findall(r"https://www\.homedepot\.com/p/[^\s\"']+", html)

        if urls:
            best_url = urls[0].split("?")[0]

            return {
                "title": item_name,
                "url": best_url,
                "confidence": 0.75
            }

        # fallback (NEVER return None)
        return {
            "title": item_name,
            "url": "https://www.homedepot.com/",
            "confidence": 0.1
        }

    except Exception:
        return {
            "title": item_name,
            "url": "https://www.homedepot.com/",
            "confidence": 0.0
        }
