# System Name

## Overview

Welcome to my submission for the Stark Bank Back End Developer Trials!

The system is designed to handle financial operations using the StarkBank SDK. It simulates a real-world application by issuing 8 to 12 invoices every 3 hours to random people for 24 hours. The StarkBank Sandbox emulation environment ensures that some of these invoices are automatically paid.

Upon receiving the webhook callback of the Invoice credit, the system transfers the received amount (minus eventual fees) to a specific account.


## Installation

Before you start, make sure you have Python installed on your system.

1. Clone this repository to your local machine.
2. Navigate to the project directory.
3. Install the required dependencies with `pip install -r requirements.txt`.

## System explanation

### Main Application

The `main.py` file is the entry point of the application. It sets up the Stark Bank API user, starts the periodic invoice issuing process, and runs the application server.

Here's a brief description of what each part of the code does:

- The `private_key_file`, `ssl_certfile`, `ssl_keyfile`, `stark_bank_environment`, and `stark_bank_id` variables are imported from the `config.py` file.

- The `starkbank.user` is set up using the Stark Bank project ID and the private key content.

- An instance of the `FinancialOperations` class is created.

- A new thread is started that runs the `issue_invoices_periodically` method of the `FinancialOperations` instance. This method issues a random number of invoices between 8 and 12 every 3 hours for 24 hours.

- The application server is run using `uvicorn`. The server listens on port 5000. The SSL key and certificate files are used to set up a secure connection.

Please ensure that the `config.py` file is set up correctly before running the `main.py` file.

### Financial Operations

The `financial_operations.py` file contains the `FinancialOperations` class, which encapsulates the financial operations of the application.

Here's a brief description of what each method does:

- `transfer_funds(invoice_id: str, amount: int)`: This method creates a `Transfer` object with the given `invoice_id` and `amount`. The `invoice_id` is used as a tag for the transfer. The transfer is then created using the Stark Bank SDK.

- `issue_invoices()`: This method creates a list of `Invoice` objects with a random amount between 10 and 100. The invoice is due in 2 days. The number of invoices is also random, between 8 and 12. The invoices are then created using the Stark Bank SDK.

- `issue_invoices_periodically()`: This method calls the `issue_invoices` method every 3 hours for 24 hours.

Please ensure that the `config.py` file is set up correctly before using the `FinancialOperations` class.

### Webhook Endpoint

The `endpoints.py` file defines the webhook endpoint for the application. It uses the FastAPI framework to create an HTTP server and define the `/webhook/` endpoint.

Here's a brief description:

- If the signature is invalid, an `InvalidSignatureError` is raised, and a 400 Bad Request response is returned.

- If the signature is valid, the type of the event is checked. If it's an `invoice` event and the type of the log is `credited`, the `transfer_funds` method of the `FinancialOperations` instance is called. The ID and the amount of the invoice (minus the fee) are passed as parameters.

- A 200 OK response is returned.

Please ensure that the `config.py` file is set up correctly before running the `endpoints.py` file.

## Configuration

The `config.py` file is used to store configuration variables for the system. These variables are fetched from the environment variables set in your system. Here's a brief description of each variable:

- `ssl_keyfile`: This is the path to the SSL key file used for secure connections. You should set this as an environment variable named `SSL_KEYFILE`.

- `ssl_certfile`: This is the path to the SSL certificate file used for secure connections. You should set this as an environment variable named `SSL_CERTFILE`.

- `private_key_file`: This is the path to the private key file used for Stark Bank API authentication. You should set this as an environment variable named `PRIVATE_KEY_FILE`.

- `stark_bank_environment`: This is the environment for the Stark Bank API. It can be either `sandbox` for testing or `production` for real transactions. You should set this as an environment variable named `STARK_BANK_ENV`.

- `stark_bank_id`: This is your Stark Bank project's ID. You should set this as an environment variable named `STARK_BANK_ID`.

Please ensure these environment variables are set correctly in your system before running the application.

## Running Tests

This project uses `pytest` for testing.

```bash
pytest