# -*- coding: utf-8 -*-
"""

Yo single tap bar recommendation
Yo Docs: http://docs.justyo.co
Yo Keys: http://dev.justyo.co

Yelp code from https://github.com/Yelp/yelp-api/blob/master/v2/python/sample.py
Yelp Docs: http://www.yelp.com/developers/documentation
Yelp Keys: http://www.yelp.com/developers/manage_api_keys

"""
import argparse
import json
import pprint
import sys
import urllib
import urllib2
import requests
import oauth2
from flask import request

API_HOST = 'api.yelp.com'
SEARCH_LIMIT = 1
SEARCH_PATH = '/v2/search/'
BUSINESS_PATH = '/v2/business/'

# OAuth credential placeholders that must be filled in by users.
# Yelp Keys: http://www.yelp.com/developers/manage_api_keys
CONSUMER_KEY = ''
CONSUMER_SECRET = ''
TOKEN = ''
TOKEN_SECRET = ''


def do_request(host, path, url_params=None):
    """Prepares OAuth authentication and sends the request to the API.

    Args:
        host (str): The domain host of the API.
        path (str): The path of the API after the domain.
        url_params (dict): An optional set of query parameters in the request.

    Returns:
        dict: The JSON response from the request.

    Raises:
        urllib2.HTTPError: An error occurs from the HTTP request.
    """
    url_params = url_params or {}
    encoded_params = urllib.urlencode(url_params)

    url = 'http://{0}{1}?{2}'.format(host, path, encoded_params)

    consumer = oauth2.Consumer(CONSUMER_KEY, CONSUMER_SECRET)
    oauth_request = oauth2.Request('GET', url, {})
    oauth_request.update(
        {
            'oauth_nonce': oauth2.generate_nonce(),
            'oauth_timestamp': oauth2.generate_timestamp(),
            'oauth_token': TOKEN,
            'oauth_consumer_key': CONSUMER_KEY
        }
    )
    token = oauth2.Token(TOKEN, TOKEN_SECRET)
    oauth_request.sign_request(oauth2.SignatureMethod_HMAC_SHA1(), consumer, token)
    signed_url = oauth_request.to_url()

    print 'Querying {0} ...'.format(signed_url)

    conn = urllib2.urlopen(signed_url, None)
    try:
        response = json.loads(conn.read())
    except Exception as e:
        print e.message
    finally:
        conn.close()

    return response

def search(term, city, latitude, longitude):
    
    url_params = {
        'term': term,
        'location': city,
        'cll': latitude + ',' + longitude,
        'limit': SEARCH_LIMIT,
        'sort': 2, # highest rated
        'radius_filter': 1600 # one mile
    }

    return do_request(API_HOST, SEARCH_PATH, url_params=url_params)


from flask import Flask
app = Flask(__name__)

@app.route("/yo/")
def yo():
    username = request.args.get('username')
    location = request.args.get('location')
    splitted = location.split(';')
    latitude = splitted[0]
    longitude = splitted[1]

    response = requests.get('http://nominatim.openstreetmap.org/reverse?format=json&lat=' + latitude + '&lon=' +longitude + '&zoom=18&addressdetails=1')
    response_object = json.loads(response.text)
    city = response_object['address']['city']

    response = search('bars', city, latitude, longitude)
    bar_url = response['businesses'][0]['mobile_url']
    requests.post("http://api.justyo.co/yo/", data={'api_token': '<your_token>', 'username': username, 'link': bar_url})
    return 'OK'

if __name__ == "__main__":
    app.debug = True
    app.run()
