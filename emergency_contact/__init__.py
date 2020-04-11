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
        ("Hayley Denbraver is looking for her next opportunity",),
        ("Hire her for Developer Advocacy, Technical Content Writing, or Python Development",),
        ('Contact her @hayleydenb on Twitter, or find further information at https://dev.to/hayleydenb'),
    ],
}
ACCEPTED_NUMBERS = [TWIL_NUMBER, TWIL_EXAMPLE_NUMBER]

def main(req: func.HttpRequest) -> func.HttpResponse:
    
    # This determines what phone number is texting my twilio number and whether they are texting my sample or emergency number.
    # I am also getting incoming text body, which will be used to properly respond. 
    send_to = req.params['From']
    send_from = req.params['To']
    incoming_message = req.params['Body'].lower()

    # We run a security check to be sure of the following:
    # 1. That someone didn't set up a twilio number to hit my site.
    # 2. That the person texting my number is authorized to do so. We don't want to give health info to a 'wrong number'

    security_check()

    # These variables help construct the proper outgoing messages.
    
    is_sample = is_sample(req)
    emergency_info = SAMPLE_INFORMATION if is_sample else EMERGENCY_INFORMATION
    outgoing_message = ""

    logging.info(log_incoming_text(is_sample, send_to)

    if incoming_message == "details":
        for detail in DETAILS:
            outgoing_message = f"{outgoing_message} {detail} \n"
    
    elif incoming_message == "meds":
        for med in MEDS:
            outgoing_message = f"{outgoing_message} {med[0]}: {med[1]} \n"
    
    elif incoming_message == "contacts":
        for contact in CONTACTS:
            outgoing_message = f"{outgoing_message} {contact[0]}: {contact[1]} \n"
    
    else:
        outgoing_message = """You have requested emergency information for Hayley Denbraver.\n\n"
        /"- Text 'detail' for medical details like allergies and known conditions.\n\n"
        /"
        
        - Text 'meds' for a list of current medications.
        
        - Text 'contacts' for a list of emergency contacts.
        
        - Text 'notify' to send Hayley's contacts a message with your phone number."""

    message = client.messages.create(
        body=outgoing_message,
        from_=TWIL_NUMBER,
        to=who_is_this,
        )


def is_sample(req):
    which_number = req.params.get['To']
    

def log_incoming_text(is_sample, send_to):
    sample_or_emergency = 'Sample' if is_sample else 'Emergency'
    return f'{sample_or_emergency} information was requested from {send_to}'