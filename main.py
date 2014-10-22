# -*- coding: utf-8 -*-
"""

Yo single tap bar recommendation
Yo Docs: http://docs.justyo.co
Yo Keys: http://dev.justyo.co

Yelp code from https://github.com/Yelp/yelp-api/blob/master/v2/python/sample.py
Yelp Docs: http://www.yelp.com/developers/documentation
Yelp Keys: http://www.yelp.com/developers/manage_api_keys

"""
import sys
import requests
import oauth2
from flask import request, Flask

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

# Yo API Token: http://dev.justyo.co
YO_API_TOKEN = ''


if len(CONSUMER_KEY) == 0 or \
    len(CONSUMER_SECRET) == 0 or \
    len(TOKEN) == 0 or \
    len(TOKEN_SECRET) == 0 or \
    len(YO_API_TOKEN) == 0:
    print 'fill the tokens in lines 30-36'
    sys.exit(1)


def do_request(host, path, url_params=None):
    
    url = 'http://{0}{1}'.format(host, path)
    consumer = oauth2.Consumer(CONSUMER_KEY, CONSUMER_SECRET)
    oauth_request = oauth2.Request('GET', url, url_params)
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

    print 'Querying Yelp {0}'.format(signed_url)

    response = requests.get(signed_url)
    response_object = response.json()
    return response_object

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


app = Flask(__name__)


@app.route("/yo/")
def yo():

    # extract and parse query parameters
    username = request.args.get('username')
    location = request.args.get('location')
    splitted = location.split(';')
    latitude = splitted[0]
    longitude = splitted[1]

    print "We got a Yo from " + username

    # get the city name since Yelp api must be provided with at least a city even though we give it accurate coordinates
    response = requests.get('http://nominatim.openstreetmap.org/reverse?format=json&lat=' + latitude + '&lon=' +longitude + '&zoom=18&addressdetails=1')
    response_object = response.json()
    city = response_object['address']['city']

    print username + " is at " + city

    # search for bars using Yelp api
    response = search('bars', city, latitude, longitude)

    # grab the first result (we limit the results to 1 anyway in the request)
    bar = response['businesses'][0]

    bar_url = bar['mobile_url']

    print "Recommended bar is " + bar['name']

    # Yo the result back to the user
    requests.post("http://api.justyo.co/yo/", data={'api_token': YO_API_TOKEN, 'username': username, 'link': bar_url})

    # OK!
    return 'OK'


if __name__ == "__main__":
    app.debug = True
    app.run(host="0.0.0.0", port=5000)
