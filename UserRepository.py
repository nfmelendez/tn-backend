# dynamodb_persistence.py

import boto3
from botocore.exceptions import NoCredentialsError, PartialCredentialsError

class UserRepository:
    def __init__(self, endpoint_url='http://localhost:8000'):
        self.dynamodb = boto3.resource('dynamodb', endpoint_url=endpoint_url)
        self.table = self.dynamodb.Table(table_name)

    def get_user(self, username):


