from flask import Flask, request, jsonify
from dotenv import load_dotenv
import json

import asyncio
import nest_asyncio

from gemini import generate_text, sentiment_analysis
from facebook import post_facebook
from scrapetiki import scrape
from wcapi.products import create_products
from wcapi.productreviews import list_all_reviews, test

load_dotenv()
nest_asyncio.apply()

app = Flask(__name__)


@app.route("/postFb", methods=["POST"])
def post_fb():
    req = request.get_json()

    post_facebook(req)

    return jsonify({"data": "success"}), 201


@app.route("/postFbWithGemini", methods=["POST"])
def post_fb_with_gemini():
    req = request.get_json()

    message = (
        "Viết một post Facebook về sản phẩm gấu bông tên"
        + req["message"]
        + "cho Fluffy Bunny với Link web của Fluffy Bunny là https://nhom4jlc.io.vn/"
    )
    text = generate_text(message)

    post_facebook({"message": text, "url": req["url"]})

    return jsonify({"data": "success"}), 201


@app.route("/scrape", methods=["POST"])
async def scrape_tiki():

    req = request.get_json()

    product_list_data = json.loads(scrape(req["number"]))

    async def post_fb_iteration_task(product_list):
        for product in product_list:
            text = generate_text(
                "Viết một post Facebook về sản phẩm gấu bông tên"
                + product["name"]
                + "cho Fluffy Bunny với Link web của Fluffy Bunny là https://nhom4jlc.io.vn/"
            )

            post_facebook({"message": text, "url": product["images"][0]["base_url"]})

    async def create_products_task():
        create_products(
            [
                {
                    "sku": product["sku"],
                    "name": product["name"],
                    "type": "simple",
                    "description": product["description"],
                    "regular_price": product["original_price"],
                    "images": [
                        {"src": image["base_url"]} for image in product["images"]
                    ],
                }
                for product in product_list_data
            ]
        )

    loop = asyncio.get_running_loop()

    tasks = [
        loop.create_task(post_fb_iteration_task(product_list_data)),
        loop.create_task(create_products_task()),
    ]

    await asyncio.gather(*tasks)

    return jsonify({"data": "success"}), 201

@app.route("/feedback", methods=["POST"])
async def feedback():
    review_list = list_all_reviews()

    async def sentiment_analysis_tasks(review_list):
        result = []
        for review in review_list:
            sentiment = sentiment_analysis(review["review"])
            result.append({
                sentiment: review
            })

        return result

    
    loop = asyncio.get_running_loop()

    review_sentiment_list = await loop.create_task(sentiment_analysis_tasks(review_list))

    reviews = {"positive": [], "negative": [], "neutral": []}

    print(review_sentiment_list)
    for review in review_sentiment_list:
        if "positive" in review:
            reviews["positive"].append(review["positive"])
        elif "negative" in review:
            reviews["negative"].append(review["negative"])
        elif "neutral" in review:
            reviews["neutral"].append(review["neutral"])

    print(test(reviews["positive"][0]["id"]))

    return jsonify({"data": reviews}), 201


if __name__ == "__main__":
    app.run(debug=True)
