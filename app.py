import os

import boto3
from flask import Flask, jsonify, make_response, request
from flask_cors import CORS
import math
import json

from  repositories.user_repository import UserRepository
from repositories.operation_repository import OperationRepository
from repositories.record_repository import RecordRepository
from services.random_string_service import RandomStringService

#SERVERLESS: https://github.com/serverless/serverless
#CORS: https://medium.com/@ernestocullen/cors-7b3243577593

app = Flask(__name__)

CORS(app)

VERSION = 'v1'

# 6 digits precision
PRECISION = 1000000

user_repo = UserRepository()

operation_repo = OperationRepository()

record_repo = RecordRepository()

random_service = RandomStringService()

@app.route(f'/{VERSION}/add', methods=['POST'])
def add():
    
    # Ideally goes in the headers but custom headers needs an extra configuration with CORS.
    username = request.json.get('App-Username')
    session =  request.json.get('App-Session')
    operation_id = "addition"
    left = int(request.json.get('left'))
    right = int(request.json.get('right'))
    def add2Number(op1, op2):
        return op1 + op2
    
    return execute_operation(add2Number, operation_id, left, right, username, session)

@app.route(f'/{VERSION}/subtraction', methods=['POST'])
def subtraction():
    
    # Ideally goes in the headers but custom headers needs an extra configuration with CORS.
    username = request.json.get('App-Username')
    session =  request.json.get('App-Session')
    operation_id = "subtraction"
    left = int(request.json.get('left'))
    right = int(request.json.get('right'))
    def subtract2Numbers(op1, op2):
        return op1 - op2
    
    return execute_operation(subtract2Numbers, operation_id, left, right, username, session)

@app.route(f'/{VERSION}/multiplication', methods=['POST'])
def multiply():
    
    # Ideally goes in the headers but custom headers needs an extra configuration with CORS.
    username = request.json.get('App-Username')
    session =  request.json.get('App-Session')
    operation_id = "multiplication"
    left = int(request.json.get('left'))
    right = int(request.json.get('right'))
    def mul(op1, op2):
        return int(op1 * op2 / PRECISION)
    
    return execute_operation(mul, operation_id, left, right, username, session)

@app.route(f'/{VERSION}/division', methods=['POST'])
def division():
    
    # Ideally goes in the headers but custom headers needs an extra configuration with CORS.
    username = request.json.get('App-Username')
    session =  request.json.get('App-Session')
    operation_id = "division"
    left = int(request.json.get('left'))
    right = int(request.json.get('right'))
    if(int(right) == 0):
        return jsonify({'error': 'Division by Zero'}), 404
    def div(op1, op2):
        return int(op1 / op2 * PRECISION)
    
    return execute_operation(div, operation_id, left, right, username, session)

@app.route(f'/{VERSION}/square_root', methods=['POST'])
def sqr_root():
    
    # Ideally goes in the headers but custom headers needs an extra configuration with CORS.
    username = request.json.get('App-Username')
    session =  request.json.get('App-Session')
    operation_id = "square_root"
    left = int(request.json.get('left'))
    def sqrt(op1, op2):
        return int(math.sqrt(op1 * PRECISION)) 
    
    return execute_operation(sqrt, operation_id, left, -1, username, session)


@app.route(f'/{VERSION}/random_string', methods=['POST'])
def random_string():
    
    # Ideally goes in the headers but custom headers needs an extra configuration with CORS.
    username = request.json.get('App-Username')
    session =  request.json.get('App-Session')
    operation_id = "random_string"
    def rnd_str(op1, op2):
        return random_service.random_string()
    
    return execute_operation(rnd_str, operation_id, -1, -1, username, session)


def execute_operation(strategy_func, operation_id, left, right, username, session):

    if user_repo.verify_session(username, session):
        # Check if users ha credit or refuse
        user = user_repo.get_user(username)
        if 'credit' in user:
            credit = user['credit']
        else:
            credit = 0

        opCost = operation_repo.operation_cost_by_id(operation_id)
        if credit >= opCost:

            result = strategy_func(left, right)
            # substract credits
            total = user_repo.substractCredit(username, opCost)
            # Register Operation
            record_repo.register_operation(username, operation=operation_id, amount=opCost, user_balance=total, operation_response=result)
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
                return jsonify({'username': username, 'session': session, 'credit': item['credit']}), 200
            else:
                # not authorize
                return jsonify({'error': 'Wrong Password'}), 403

        else:
            return jsonify({'error': 'No user: ' + username}), 404

    except Exception as e:
        return jsonify({'error': f"An error occurred: {e}"}), 500


@app.route(f'/{VERSION}/records', methods=['GET'])
def get_record_data():
    limit = int(request.args.get('limit', 10))
    last_evaluated_key = request.args.get('lastKey', None)

    if last_evaluated_key:
        last_evaluated_key = json.loads(last_evaluated_key)

    return jsonify(record_repo.record_data(limit, last_evaluated_key))

 

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