import requests
import re
import time

HEADERS = {"User-Agent": "Mozilla/5.0"}


TOOLS_CATEGORIES = [
    # Power Tools
    "https://www.homedepot.com/b/Tools-Power-Tools/N-5yc1vZc298",
    "https://www.homedepot.com/b/Tools-Power-Drills/N-5yc1vZc299",
    "https://www.homedepot.com/b/Tools-Saws/N-5yc1vZc2a1",
    "https://www.homedepot.com/b/Tools-Impact-Wrenches/N-5yc1vZc2a2",

    # Hand Tools
    "https://www.homedepot.com/b/Tools-Hand-Tools/N-5yc1vZc1xy",
    "https://www.homedepot.com/b/Tools-Hammers/N-5yc1vZc1xz",
    "https://www.homedepot.com/b/Tools-Wrenches/N-5yc1vZc1y0",

    # Outdoor Power Equipment
    "https://www.homedepot.com/b/Outdoors-Outdoor-Power-Equipment/N-5yc1vZbx8t",
    "https://www.homedepot.com/b/Outdoors-Lawn-Mowers/N-5yc1vZbx8u",
    "https://www.homedepot.com/b/Outdoors-Leaf-Blowers/N-5yc1vZbx8v",

    # Tool Storage
    "https://www.homedepot.com/b/Tools-Tool-Storage/N-5yc1vZc1xw",
]


def extract_products(html):
    """
    Pull product URLs from category page HTML
    """

    matches = re.findall(r"https://www\.homedepot\.com/p/[^\s\"']+", html)

    cleaned = []
    for m in matches:
        url = m.split("?")[0]
        if url not in cleaned:
            cleaned.append(url)

    return cleaned


def crawl_category(url, pages=5):

    results = []

    for page in range(1, pages + 1):

        try:
            paged_url = f"{url}?Nao={page * 24}"
            print(f"Scraping: {paged_url}")

            r = requests.get(paged_url, headers=HEADERS, timeout=10)

            if r.status_code != 200:
                print("Blocked or error:", r.status_code)
                continue

            products = extract_products(r.text)

            if not products:
                print("No products found — stopping pagination")
                break

            results.extend(products)

            time.sleep(1.2)

        except Exception as e:
            print("ERROR:", e)

    return results


def fetch_products():

    all_products = []

    for cat in TOOLS_CATEGORIES:

        print(f"\nCATEGORY START: {cat}")

        urls = crawl_category(cat, pages=3)

        for u in urls:

            name = u.split("/")[-1].replace("-", " ")

            all_products.append({
                "name": name.title(),
                "url": u
            })

    # deduplicate
    unique = {p["url"]: p for p in all_products}

    final = list(unique.values())

    print("\nTOTAL UNIQUE PRODUCTS:", len(final))

    return final
