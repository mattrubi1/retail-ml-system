import requests
import urllib.parse
import time

HEADERS = {"User-Agent": "Mozilla/5.0"}

SEARCH_TERMS = [
    "drill homedepot",
    "impact driver homedepot",
    "chainsaw homedepot",
    "wet dry vac homedepot",
    "tool set homedepot",
    "grinder homedepot",
    "leaf blower homedepot",
    "table saw homedepot",
]


def fetch_products():

    all_products = []

    for term in SEARCH_TERMS:

        try:
            query = urllib.parse.quote(term)

            url = f"https://duckduckgo.com/html/?q={query}"

            print(f"Searching: {term}")

            r = requests.get(url, headers=HEADERS, timeout=10)

            if r.status_code != 200:
                print("Blocked:", r.status_code)
                continue

            html = r.text

            # Extract links manually (DuckDuckGo format)
            links = []

            parts = html.split('href="')

            for part in parts:
                if "homedepot.com/p/" in part:
                    link = part.split('"')[0]

                    if link.startswith("http") and link not in links:
                        links.append(link)

            if not links:
                print("⚠️ No links found for:", term)
                continue

            for l in links[:15]:

                name = l.split("/")[-1].replace("-", " ")

                all_products.append({
                    "name": name.title(),
                    "url": l.split("?")[0]
                })

            time.sleep(1)

        except Exception as e:
            print("ERROR:", e)

    # Remove duplicates
    unique = {p["url"]: p for p in all_products}
    final = list(unique.values())

    print("✅ TOTAL PRODUCTS:", len(final))

    return final
