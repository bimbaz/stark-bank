import json
from unittest.mock import MagicMock, patch

import pytest
from fastapi import status
from starlette.testclient import TestClient

from endpoints import app


@pytest.fixture
def client():
    return TestClient(app)


@patch("endpoints.FinancialOperations")
def test_webhook(mock_financial_operations, client):
    mock_fo_instance = MagicMock()
    mock_financial_operations.return_value = mock_fo_instance

    invoice_id = "INV123"
    invoice_amount = 1000
    invoice_fee = 50

    event_data = {
        "subscription": "invoice",
        "log": {
            "type": "credited",
            "invoice": {
                "id": invoice_id,
                "amount": invoice_amount,
                "fee": invoice_fee,
            },
        },
    }

    event_json = json.dumps(event_data)
    signature = "signature"

    response = client.post(
        "/webhook/",
        headers={"Digital-Signature": signature},
        content=event_json,
    )

    assert response.status_code == status.HTTP_200_OK
    mock_financial_operations.assert_called_once_with()


@patch("endpoints.FinancialOperations")
def test_webhook_invalid_signature(mock_financial_operations, client):
    mock_fo_instance = MagicMock()
    mock_financial_operations.return_value = mock_fo_instance

    event_data = {"subscription": "invoice", "log": {"type": "credited"}}

    event_json = json.dumps(event_data)
    signature = "invalid_signature"

    response = client.post(
        "/webhook/",
        headers={"Digital-Signature": signature},
        content=event_json,
    )

    assert response.content == b'["Invalid signature",400]'
