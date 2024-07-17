from app import create_app
from unittest.mock import MagicMock

from  repositories.user_repository import UserRepository
from repositories.operation_repository import OperationRepository
from repositories.record_repository import RecordRepository
from services.random_string_service import RandomStringService


def test_user_has_no_credit():
    mock_user_repo = MagicMock()
    mock_operation_repo = MagicMock()
    mock_record_repo = MagicMock()
    mock_random_service = MagicMock()

    app = create_app(mock_user_repo, mock_operation_repo, mock_record_repo, mock_random_service)
    app.config.update({
     "TESTING": True,
    })

    c = app.test_client()


    mock_operation_repo.operation_cost_by_id.return_value = 2


    response = c.post("/v1/add", json={
        "left": "1",
        "right": "2",
    })

    assert b'{"error":"Credit not enough, credit 0, operation cost: 2"}' in response.data 
    assert response.status_code == 404


def test_sum_2_values():
    mock_user_repo = MagicMock()
    mock_operation_repo = MagicMock()
    mock_record_repo = MagicMock()
    mock_random_service = MagicMock()

    app = create_app(mock_user_repo, mock_operation_repo, mock_record_repo, mock_random_service)
    app.config.update({
     "TESTING": True,
    })

    c = app.test_client()


    mock_operation_repo.operation_cost_by_id.return_value = 0

    mock_user_repo.substractCredit.return_value = 0


    response = c.post("/v1/add", json={
        "left": "1",
        "right": "2",
    })
    
    assert b'{"credit":0,"result":3}' in response.data 
    assert response.status_code == 200

def test_request_no_records():
    mock_user_repo = MagicMock()
    mock_operation_repo = MagicMock()
    mock_record_repo = MagicMock()
    mock_random_service = MagicMock()

    app = create_app(mock_user_repo, mock_operation_repo, mock_record_repo, mock_random_service)
    app.config.update({
     "TESTING": True,
    })

    c = app.test_client()

    mock_record_repo.record_data.return_value = {
            'Items': [],
            'LastEvaluatedKey': None
        }


    response = c.get("/v1/records")
    assert b'{"Items":[],"LastEvaluatedKey":null}' in response.data 