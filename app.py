import os

import boto3
from flask import Flask, jsonify, make_response, request
from flask_cors import CORS

from  repositories.user_repository import UserRepository


#CORS: https://medium.com/@ernestocullen/cors-7b3243577593
app = Flask(__name__)

CORS(app)

VERSION = 'v1'

user_repo = UserRepository()


@app.route(f'/{VERSION}/add', methods=['POST'])
def add():
    
    # Ideally goes in the headers but custom headers needs an extra configuration with CORS.
    username = request.json.get('App-Username')
    session =  request.json.get('App-Session')

    if user_repo.verify_session(username, session):
        # Check if users ha credit or refuse
        user = user_repo.get_user(username)
        if 'credit' in user:
            credit = user['credit']
        else:
            credit = 0

        # TODO: fetch operation cost
        opCost = 2
        if credit >= opCost:
            left = request.json.get('left')
            right = request.json.get('right')
            result = left + right
            # substract credits
            total = user_repo.substractCredit(username, opCost)
            # Register Operation
            return jsonify(
                {'result': result, 'credit': total}
            )
        else:
            return jsonify({'error': f'Credit not enough, credit {credit}, operation cost: {opCost}'}), 404    
    else:
       return jsonify({'error': f'Invalid session {session} for username {username}'}), 403 


@app.route(f'/{VERSION}/user/login', methods=['POST'])
def login_user():
    username = request.json.get('username')
    password = request.json.get('password')
    if not username or not password:
        return jsonify({'error': 'Please provide both "username" and "password"'}), 404
    
    try:

        item = user_repo.get_user(username)

        if item:
            #Password is not hashed, would be lot better to be hashed
            if item['password'] == password:
                import uuid
                session = str(uuid.uuid4())
                # Session never expire or the user make it expire. But is better to add an automatic expiration in time.
                user_repo.update_session(username, session)
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
#  "status": "active",
#  "credit": 100
# }


# {
#   "username": {
#     "S": "john@gmail.com"
#   },
#   "credit": {
#     "N": "998"
#   },
#   "password": {
#     "S": "123"
#   },
#   "status": {
#     "S": "active"
#   },
#   "user_session": {
#     "S": "b5d4dccb-3eec-4812-bc3d-a3697999ce7c"
#   }
# }