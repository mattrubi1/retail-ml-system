import requests

HEADERS = {
    "User-Agent": "Mozilla/5.0",
    "Accept": "application/json"
}

# REAL Home Depot API endpoint (used internally)
API_URL = "https://www.homedepot.com/federation-gateway/graphql"


def fetch_products():

    products = []

    # GraphQL payload (tools category)
    payload = {
        "operationName": "search",
        "variables": {
            "searchTerm": "tools",
            "storeId": "1280",
            "pageSize": 24
        },
        "query": """
        query search($searchTerm: String!, $storeId: String!, $pageSize: Int!) {
          search(searchTerm: $searchTerm, storeId: $storeId, pageSize: $pageSize) {
            products {
              items {
                productId
                identifiers {
                  canonicalUrl
                }
                itemName
                pricing {
                  value
                }
              }
            }
          }
        }
        """
    }

    try:
        r = requests.post(API_URL, json=payload, headers=HEADERS, timeout=10)

        if r.status_code != 200:
            print("❌ API failed:", r.status_code)
            return []

        data = r.json()

        items = data["data"]["search"]["products"]["items"]

        for item in items:

            try:
                url = "https://www.homedepot.com" + item["identifiers"]["canonicalUrl"]

                products.append({
                    "name": item["itemName"],
                    "url": url
                })
            except:
                continue

    except Exception as e:
        print("ERROR:", e)

    print("✅ PRODUCTS FOUND:", len(products))

    return products
