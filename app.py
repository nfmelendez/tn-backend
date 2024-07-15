import os

import boto3
from flask import Flask, jsonify, make_response, request

from flask_cors import CORS

#CORS: https://medium.com/@ernestocullen/cors-7b3243577593
app = Flask(__name__)

CORS(app)

VERSION = 'v1'


dynamodb = boto3.resource('dynamodb')

if os.environ.get('IS_OFFLINE'):
    dynamodb = boto3.resource('dynamodb', endpoint_url='http://localhost:8000')



USERS_TABLE = os.environ['USERS_TABLE']

@app.route(f'/{VERSION}/add', methods=['POST'])
def add():
    # Check if users ha credit or refuse
    left = request.json.get('left')
    right = request.json.get('right')
    result = left + right
    # Discount credits
    # Register Operation
    return jsonify(
        {'result': result}
    )


@app.route(f'/{VERSION}/user/login', methods=['POST'])
def login_user():
    username = request.json.get('username')
    password = request.json.get('password')
    if not username or not password:
        return jsonify({'error': 'Please provide both "username" and "password"'}), 404
    
    try:
        table = dynamodb.Table(USERS_TABLE)
        
        # Get the item from the table
        response = table.get_item(
            Key={
                'username': username
            }
        )

        item = response.get('Item')

        if item:
            #Password is not hashed, would be lot better to be hashed
            if item['password'] == password:
                import uuid
                session = str(uuid.uuid4())
                # Session never expire or the user make it expire. But is better to add an automatic expiration in time. 
                return jsonify({'username': username, 'session': session}), 200
            else:
                # not authorize
                return jsonify({'error': 'Wrong Password'}), 403

        else:
            return jsonify({'error': 'No user: ' + username}), 404

    except Exception as e:
        return jsonify({'error': f"An error occurred: {e}"}), 500



@app.errorhandler(404)
def resource_not_found(e):
    return make_response(jsonify(error='Not found!'), 404)



# user db
# {
#  "username": "john@gmail.com",
#  "password": "123",
#  "status": "active"
# }