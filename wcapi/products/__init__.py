import os

from woocommerce import API


def create_products(product_list):

    wcapi = API(
        url=os.getenv("WP_URL"),
        consumer_key=os.getenv("WP_CK"),
        consumer_secret=os.getenv("WP_CS"),
        wp_api=True,
        version="wc/v3",
        timeout=120,
    )

    data = {"create": product_list}

    wcapi.post("products/batch", data)
