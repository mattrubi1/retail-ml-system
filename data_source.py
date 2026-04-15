from category_graph import crawl


def fetch_products():

    urls = crawl(max_depth=2)

    products = []

    for u in urls:

        name = u.split("/")[-1].replace("-", " ")

        products.append({
            "name": name.title(),
            "url": u.split("?")[0]
        })

    return products
