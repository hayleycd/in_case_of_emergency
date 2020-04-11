import logging

import azure.functions as func
from twilio.rest import Client

# Environment variables

ACCOUNT_SID = os.environ['ACCOUNT_SID']
AUTH_TOKEN = os.environ['AUTH_TOKEN']
TWIL_NUMBER = os.environ['TWIL_NUMBER']
TWIL_EXAMPLE_NUMBER = os.environ['TWIL_EXAMPLE_NUMBER']
EMERGENCY_PIN = os.environ['EMERGENCY_PIN']
EMERGENCY_INFORMATION = os.environ['EMERGENCY_INFORMATION']
SAMPLE_INFORMATION = {}

# Global variables

CLIENT = Client(ACCOUNT_SID, AUTH_TOKEN)

def main(req: func.HttpRequest) -> func.HttpResponse:
    is_sample = sample_or_real(req)

    if is_sample:
        run_sample_workflow(req)
    else:
        run_workflow(req)

    logging.info('Python HTTP trigger function processed a request.')

    name = req.params.get('name')
    if not name:
        try:
            req_body = req.get_json()
        except ValueError:
            pass
        else:
            name = req_body.get('name')

    if name:
        return func.HttpResponse(f"Hello {name}!")
    else:
        return func.HttpResponse(
             "Please pass a name on the query string or in the request body",
             status_code=400
        )

def sample_or_real(req):
    req.params.get['To']

def run_sample_workflow(req):
    pass

def run_workflow(req):
    pass