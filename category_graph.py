import requests
import re
import time

HEADERS = {"User-Agent": "Mozilla/5.0"}

SEED_CATEGORIES = [
    "https://www.homedepot.com/b/Tools/N-5yc1vZc1xy",
]


def extract_links(html):

    # capture category links
    return list(set(re.findall(
        r"https://www\.homedepot\.com/b/[^\s\"']+",
        html
    )))


def extract_products(html):

    return list(set(re.findall(
        r"https://www\.homedepot\.com/p/[^\s\"']+",
        html
    )))


def crawl(max_depth=2):

    visited = set()
    to_visit = SEED_CATEGORIES

    all_products = set()

    for depth in range(max_depth):

        print(f"\nDEPTH LEVEL: {depth} | URLs: {len(to_visit)}")

        next_level = []

        for url in to_visit:

            if url in visited:
                continue

            visited.add(url)

            try:
                r = requests.get(url, headers=HEADERS, timeout=10)

                if r.status_code != 200:
                    continue

                html = r.text

                # collect products
                products = extract_products(html)
                for p in products:
                    all_products.add(p.split("?")[0])

                # collect subcategories
                cats = extract_links(html)
                next_level.extend(cats)

                time.sleep(1)

            except Exception as e:
                print("ERROR:", e)

        to_visit = list(set(next_level))

    print("\nTOTAL PRODUCTS FOUND:", len(all_products))

    return list(all_products)
