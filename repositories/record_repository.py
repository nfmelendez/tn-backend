# dynamodb_persistence.py
import os

import boto3
from botocore.exceptions import NoCredentialsError, PartialCredentialsError
from datetime import datetime, timezone
import uuid

#DATA STRUCTURE:
# ○ id
# ○ operation_id
# ○ user_id
# ○ amount
# ○ user_balance
# ○ operation_response
# ○ date
class RecordRepository:
    def __init__(self):
        self.dynamodb = boto3.resource('dynamodb')
        if os.environ.get('IS_OFFLINE'):
            self.dynamodb = boto3.resource('dynamodb', endpoint_url='http://localhost:8000')
        RECORD_TABLE = os.environ['RECORD_TABLE']
        self.table = self.dynamodb.Table(RECORD_TABLE)

    def register_operation(self, username, operation, amount, user_balance, operation_response):

        item = {
            'id': str(uuid.uuid4()),
            'operation_id': operation,
            'username': username,
            'amount': amount,
            'user_balance': user_balance,
            'operation_response': operation_response,
            'date': datetime.now(timezone.utc).isoformat() + 'Z',  # ISO 8601 format
        }

        self.table.put_item(Item=item)


    def record_data(self, limit, last_key):
        if last_key is None:
            response = self.table.scan(
            Limit=limit
            )
        else:    
            response = self.table.scan(
                Limit=limit,
                ExclusiveStartKey=last_key
            )

        items = response.get('Items', [])
        last_evaluated_key = response.get('LastEvaluatedKey', None)

        return {
            'Items': items,
            'LastEvaluatedKey': last_evaluated_key
        }