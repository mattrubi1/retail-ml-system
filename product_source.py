import requests
import urllib.parse
import re
import time

HEADERS = {"User-Agent": "Mozilla/5.0"}

SEARCH_TERMS = [
    "drill site:homedepot.com",
    "impact driver site:homedepot.com",
    "chainsaw site:homedepot.com",
    "wet dry vac site:homedepot.com",
    "tool set site:homedepot.com",
    "grinder site:homedepot.com",
    "leaf blower site:homedepot.com",
    "table saw site:homedepot.com",
]


def extract_links(html):

    matches = re.findall(r"https://www\.homedepot\.com/p/[^\s\"<>]+", html)

    cleaned = []
    for m in matches:
        url = m.split("&")[0]
        if url not in cleaned:
            cleaned.append(url)

    return cleaned


def fetch_products():

    all_products = []

    for term in SEARCH_TERMS:

        try:
            query = urllib.parse.quote(term)
            url = f"https://www.bing.com/search?q={query}"

            print(f"Searching Bing: {term}")

            r = requests.get(url, headers=HEADERS, timeout=10)

            if r.status_code != 200:
                print("Blocked:", r.status_code)
                continue

            links = extract_links(r.text)

            if not links:
                print("⚠️ No links found")
                continue

            for l in links[:20]:

                name = l.split("/")[-1].replace("-", " ")

                all_products.append({
                    "name": name.title(),
                    "url": l
                })

            time.sleep(1)

        except Exception as e:
            print("ERROR:", e)

    # dedupe
    unique = {p["url"]: p for p in all_products}

    final = list(unique.values())

    print("✅ TOTAL PRODUCTS FOUND:", len(final))

    return final
