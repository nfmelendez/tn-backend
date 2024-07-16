# dynamodb_persistence.py
import os
import requests
import json

class RandomStringService:
    def __init__(self):
        self.apiKey = os.environ.get('RANDOM_ORG_API_KEY')
        self.request_counter = 1

    def random_string(self):
        print(f'Api key: {self.apiKey}')
        raw_data = {
            "jsonrpc": "2.0",
            "method": "generateStrings",
            "params": {
                "apiKey": self.apiKey,
                "n": 1,
                "length": 10,
                "characters": "abcdefghijklmnopqrstuvwxyz",
                "replacement": True
            },
            'id': self.request_counter
        }

        headers = {'Content-type': 'application/json','Content-Length': '200', 'Accept': 'application/json'}

        data=json.dumps(raw_data)

        response = requests.post(
            url='https://api.random.org/json-rpc/2/invoke',
            data=data,
            headers=headers
            )
        self.request_counter += 1
        resp_json = json.loads(response.text)

        # 1. Should check if the the request is success or not, we asumme always success.
        # 2. The request should have a timeout so this service doesn't depend on third=parties slow to respond.
        r = resp_json['result']['random']['data']
        return r
