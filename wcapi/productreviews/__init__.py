import os

from woocommerce import API

def init():
    return API(
        url=os.getenv("WP_URL"),
        consumer_key=os.getenv("WP_CK"),
        consumer_secret=os.getenv("WP_CS"),
        wp_api=True,
        version="wc/v3",
        timeout=120,
    )

def list_all_reviews():
    wcapi = init()

    res = wcapi.get("products/reviews").json()

    return res

def test(id):
    wcapi = init()

    res = wcapi.put(f"products/reviews/{id}", {
        "rating": 5
    }).json()

    return res
    