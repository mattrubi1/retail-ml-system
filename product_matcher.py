import requests
import urllib.parse
import re

HEADERS = {"User-Agent": "Mozilla/5.0"}


def match_product(item_name: str):

    try:
        query = urllib.parse.quote(f"site:homedepot.com {item_name}")

        url = f"https://duckduckgo.com/html/?q={query}"

        r = requests.get(url, headers=HEADERS, timeout=10)
        html = r.text

        # Extract any Home Depot product link
        matches = re.findall(r"https://www\.homedepot\.com/[^\s\"']+", html)

        if not matches:
            return {
                "title": None,
                "url": None,
                "confidence": 0
            }

        clean_url = matches[0].split("?")[0]

        confidence = 0.7 if "/p/" in clean_url else 0.4

        return {
            "title": item_name,
            "url": clean_url,
            "confidence": confidence
        }

    except Exception:
        return {
            "title": None,
            "url": None,
            "confidence": 0
        }
