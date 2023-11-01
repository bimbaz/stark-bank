from unittest.mock import MagicMock, patch

import pytest

from financial_operations import FinancialOperations


@pytest.fixture
def financial_operations():
    return FinancialOperations()


@patch("financial_operations.starkbank.transfer.create")
def test_transfer_funds(mock_transfer_create, financial_operations):
    invoice_id = "INV123"
    amount = 1000

    mock_transfer = MagicMock()
    mock_transfer.id = "TRF123"
    mock_transfer_create.return_value = [mock_transfer]

    financial_operations.transfer_funds(invoice_id, amount)


@patch("financial_operations.starkbank.invoice.create")
def test_issue_invoices(mock_invoice_create, financial_operations):
    mock_invoice = MagicMock()
    mock_invoice_create.return_value = [mock_invoice]

    financial_operations.issue_invoices()

    assert mock_invoice_create.call_count == 1
    assert len(mock_invoice_create.call_args[0][0]) >= 8
    assert len(mock_invoice_create.call_args[0][0]) <= 12
