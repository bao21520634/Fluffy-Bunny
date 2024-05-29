import os

import requests

pageId = os.getenv('PAGE_ID')

def post_facebook(object):
    requests.post(f'https://graph.facebook.com/v20.0/{pageId}/photos', json={
        "access_token": os.getenv('META_ACCESS_TOKEN'),
        **object
    })