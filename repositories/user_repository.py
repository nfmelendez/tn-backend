# dynamodb_persistence.py
import os

import boto3
from botocore.exceptions import NoCredentialsError, PartialCredentialsError

# DATA STRUCTURE:
# ○ id
# ○ username (email)
# ○ password
# ○ status (active, inactive)
class UserRepository:
    def __init__(self):
        self.dynamodb = boto3.resource('dynamodb')
        if os.environ.get('IS_OFFLINE'):
            self.dynamodb = boto3.resource('dynamodb', endpoint_url='http://localhost:8000')
        USERS_TABLE = os.environ['USERS_TABLE']
        self.table = self.dynamodb.Table(USERS_TABLE)

    def get_user(self, username):
        response = self.table.get_item(
            Key={
                'username': username
            }
        )

        item = response.get('Item')
        return item

    def update_session(self, username, session):
        key = {
            'username': username
        }

        response = self.table.update_item(
            Key=key,
            UpdateExpression=f"set user_session = :value",
            ExpressionAttributeValues={
                ':value': session
            },
            ReturnValues="UPDATED_NEW"
        )
        return response

    def verify_session(self, username, session):
        user = self.get_user(username)
        return session == user['user_session']
    


    def substractCredit(self, username, opCost):
        key = {
            'username': username
        }
        response = self.table.update_item(
            Key=key,
            UpdateExpression=f"set credit = credit - :value",
            ExpressionAttributeValues={
                ':value': opCost
            },
            ReturnValues="UPDATED_NEW"
        )
        updated_attributes = response.get('Attributes', {})
        updated_credit = updated_attributes.get('credit', None)
        return int(updated_credit)
        