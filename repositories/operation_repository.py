# dynamodb_persistence.py
import os

import boto3

# Data Struucture:
# id
# type (addition, subtraction, multiplication, division, square_root, random_string)
# cost
# Example
# {
#   "id": {
#     "S": "addition"
#   },
#   "cost": {
#     "N": "2"
#   },
#   "type": {
#     "S": "addition"
#   }
# }
class OperationRepository:
    def __init__(self):
        self.dynamodb = boto3.resource('dynamodb')
        if os.environ.get('IS_OFFLINE'):
            self.dynamodb = boto3.resource('dynamodb', endpoint_url='http://localhost:8000')
        OPERATION_TABLE = os.environ['OPERATION_TABLE']
        self.table = self.dynamodb.Table(OPERATION_TABLE)

    def operation_cost_by_id(self, operation_id):
        response = self.table.get_item(
            Key={
                'id': operation_id
            }
        )

        item = response.get('Item')
        return item['cost']
