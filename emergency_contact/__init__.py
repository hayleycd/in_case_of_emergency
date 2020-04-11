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
NAME = os.environ['NAME']


# Global variables

CLIENT = Client(ACCOUNT_SID, AUTH_TOKEN)
SAMPLE_INFORMATION = {
    'meds': [
        ('Med A', 'Notes for A'),
        ('Med B', 'Notes for B'),
        ('Med C', 'Notes for C'),
    ],
    'details': [
        ('Blood type', 'Blood type here'),
        ('Allergies', 'List of Allergies'),
        ('Other information', 'Conditions and/or additional information'),
    ],
    'contacts': [
        ('Contact D', 'Contact D phone number'),
        ('Contact E', 'Contact E phone number'),
        ('Contact F', 'Contact F phone number'),
    ],
    'hire': [
        ("Hayley is looking for her next opportunity",),
        ("Hire her for Developer Advocacy, Technical Content Writing, or Python Development",),
        ('Contact her @hayleydenb on Twitter, or find further information at https://dev.to/hayleydenb'),
    ],
}

def main(req: func.HttpRequest) -> func.HttpResponse:
    emergency_info = SAMPLE_INFORMATION if is_sample(req) else EMERGENCY_INFORMATION

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