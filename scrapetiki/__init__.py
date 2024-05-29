import json
import re

import aiohttp
import asyncio
import json

dict_product = {"teddy-bear": "https://tiki.vn/api/v2/products?q=gau+bong&page={page}"}

product_api_url = "https://tiki.vn/api/v2/products/{id}"

digit = re.compile(r"\d+")

headers = {"user-agent": "my-app/0.0.1", "Content-Type": "application/json"}

async def scrape_product_id(number):
    product_list = []

    page_index = 0
    for type_product in dict_product:
        while True:
            print(f"Product {type_product}: {page_index+1}".format(type_product))

            async with aiohttp.ClientSession() as session:
                async with session.get(
                    dict_product[type_product].format(page=page_index + 1),
                    headers=headers,
                ) as response:
                    if response.status == 200:
                        content = await response.json()
                        list_products = content.get("data")
                        for product in list_products:
                            product_list.append(str(product.get("id")))
                            if len(product_list) == number:
                                return product_list
        
            page_index += 1
    


async def scrape_product(list_products=[]):
    product_detail_list = []
    for product_id in list_products:
        async with aiohttp.ClientSession() as session:
            async with session.get(
                product_api_url.format(id=product_id), headers=headers
            ) as response:
                if response.status == 200:
                    if "application/json" in response.headers.get("Content-Type", ""):
                        content = await response.json()
                        product_detail_list.append(content)
                        print("scrape product: ", product_id, " --> ", response.status)
    return product_detail_list


async def main(number):
    product_id_list = await scrape_product_id(number)

    # scrape product and save to file
    product_list = await scrape_product(product_id_list)

    with open("./output/product_data_import.json", mode="w") as f:
        f.write(json.dumps(product_list))
        f.close()

    return json.dumps(product_list)


def scrape(number):
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    product_list = loop.run_until_complete(main(number))
    return product_list
