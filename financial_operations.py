import random
from datetime import datetime, timedelta
from time import sleep

import starkbank


class FinancialOperations:
    def transfer_funds(self, invoice_id: str, amount: int):
        transfers = starkbank.transfer.create(
            [
                starkbank.Transfer(
                    amount=amount,
                    bank_code="20018183",
                    branch_code="0001",
                    account_number="6341320293482496",
                    account_type="payment",
                    tax_id="20.018.183/0001-80",
                    name="Stark Bank S.A.",
                    tags=[invoice_id],
                )
            ]
        )
        for transfer in transfers:
            print(f"Transfer created: {transfer.id}")

    def issue_invoices(self):
        invoices = []
        for _ in range(random.randint(8, 12)):
            invoices.append(
                starkbank.Invoice(
                    amount=random.randint(1000, 10000),
                    tax_id="20.018.183/0001-80",
                    name="Random Customer",
                    due=datetime.now() + timedelta(days=2),
                    tags=["sdk", "test"],
                )
            )
        print(f"Issuing {len(invoices)} invoices")
        starkbank.invoice.create(invoices)

    def issue_invoices_periodically(self):
        for _ in range(8):
            self.issue_invoices()
            sleep(3 * 60 * 60)
