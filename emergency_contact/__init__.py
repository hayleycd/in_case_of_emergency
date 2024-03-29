import logging
import os
import __app__.helper as helper

import azure.functions as func
import sentry_sdk
from sentry_sdk.integrations.serverless import serverless_function

# Environment variable
SENTRY = os.environ["SENTRY_DSN"]

# Sentry
sentry_sdk.init(
    dsn=SENTRY,

    # Set traces_sample_rate to 1.0 to capture 100%
    # of transactions for performance monitoring.
    # We recommend adjusting this value in production.
    traces_sample_rate=1.0,
)

@serverless_function
def main(req: func.HttpRequest) -> func.HttpResponse:

    # This determines what phone number is texting my twilio number and whether they are texting my sample or emergency number.
    # I am also getting the incoming text body, which will be used to properly respond.
    send_to = req.params["From"]
    send_from = req.params["To"]
    incoming_message = req.params["Body"].lower().strip()

    # These variables help construct the proper outgoing messages.
    is_sample = helper.is_sample(send_from)
    emergency_info = (
        helper.SAMPLE_INFORMATION if is_sample else helper.EMERGENCY_INFORMATION
    )
    pin = helper.SAMPLE_PIN if is_sample else helper.EMERGENCY_PIN

    # This logs incoming text.
    logging.info(helper.log_incoming_text(is_sample, send_to))

    # This kicks off the logic
    helper.security_check_and_workflow(
        pin, send_to, send_from, incoming_message, is_sample, emergency_info
    )

    return func.HttpResponse(
        "You can text this number again if you need more information.", status_code=200
    )
