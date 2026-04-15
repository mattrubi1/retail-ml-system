import requests
import re

HEADERS = {"User-Agent": "Mozilla/5.0"}


CATEGORY_URLS = [
    "https://www.homedepot.com/b/Tools-Power-Tools/N-5yc1vZc298",
    "https://www.homedepot.com/b/Tools-Hand-Tools/N-5yc1vZc1xy",
    "https://www.homedepot.com/b/Outdoors-Outdoor-Power-Equipment/N-5yc1vZbx8t",
]


def extract_products_from_page(html):

    matches = re.findall(r"https://www\.homedepot\.com/p/[^\s\"']+", html)

    cleaned = []
    for m in matches:
        url = m.split("?")[0]
        if url not in cleaned:
            cleaned.append(url)

    return cleaned


def fetch_products():

    products = []

    for category in CATEGORY_URLS:

        try:
            print(f"Scraping: {category}")

            r = requests.get(category, headers=HEADERS, timeout=10)
            html = r.text

            urls = extract_products_from_page(html)

            for u in urls[:40]:  # limit per category

                name = u.split("/")[-1].replace("-", " ")

                products.append({
                    "name": name.title(),
                    "url": u
                })

        except Exception as e:
            print("ERROR:", e)

    print("TOTAL PRODUCTS:", len(products))

    return products
