from threading import Thread

import starkbank

from config import (
    private_key_file,
    ssl_certfile,
    ssl_keyfile,
    stark_bank_environment,
    stark_bank_id,
)
from endpoints import app
from financial_operations import FinancialOperations

if __name__ == "__main__":
    import uvicorn

    with open(private_key_file, "r") as file:
        private_key_content = file.read()

    starkbank.user = starkbank.Project(
        environment=stark_bank_environment,
        id=stark_bank_id,
        private_key=private_key_content,
    )

    financial_operations = FinancialOperations()

    thread = Thread(target=financial_operations.issue_invoices_periodically)
    thread.start()

    uvicorn.run(
        app,
        host="0.0.0.0",
        port=5000,
        ssl_keyfile=ssl_keyfile,
        ssl_certfile=ssl_certfile,
    )
