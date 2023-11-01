import json

import starkbank
from fastapi import FastAPI, Request, status

from financial_operations import FinancialOperations

app = FastAPI()


@app.post("/webhook/")
async def webhook(request: Request):
    financial_operations = FinancialOperations()

    try:
        event = starkbank.event.parse(
            content=json.dumps(await request.json()),
            signature=request.headers["Digital-Signature"],
        )
    except starkbank.error.InvalidSignatureError as exception:
        print(exception)
        return "Invalid signature", status.HTTP_400_BAD_REQUEST
    else:
        if event.subscription == "invoice":
            if event.log.type == "credited":
                print(f"Invoice credited: {event.log.invoice.id}")
                financial_operations.transfer_funds(
                    event.log.invoice.id,
                    event.log.invoice.amount - event.log.invoice.fee,
                )

    return "OK", status.HTTP_200_OK
