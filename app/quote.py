import os
import json
import requests

def get_quote():
    r = requests.get('http://quotes.rest/qod.json?category=inspire')

    if r.status_code != 200:
        os.environ['QUOTE_OF_THE_DAY'] = json.dumps(
            {'quote': 'Cats rule the world.',
             'author': 'Jim Davis'})
    os.environ['QUOTE_OF_THE_DAY'] = json.dumps(
        json.loads(r.content)['contents']['quotes'][0])