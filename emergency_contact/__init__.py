import logging

import azure.functions as func
from twilio.rest import Client

# Environment variables

ACCOUNT_SID = os.environ['ACCOUNT_SID']
AUTH_TOKEN = os.environ['AUTH_TOKEN']
TWIL_NUMBER = os.environ['TWIL_NUMBER']
TWIL_EXAMPLE_NUMBER = os.environ['TWIL_EXAMPLE_NUMBER']
EMERGENCY_PIN = os.environ['EMERGENCY_PIN']
SAMPLE_PIN = os.environ['SAMPLE_PIN']
EMERGENCY_INFORMATION = os.environ['EMERGENCY_INFORMATION']
NAME = os.environ['NAME']


# Global variables

CLIENT = Client(ACCOUNT_SID, AUTH_TOKEN)
SAMPLE_INFORMATION = {
    'meds': [
        ('Med A:', 'Notes for A'),
        ('Med B:', 'Notes for B'),
        ('Med C:', 'Notes for C'),
    ],
    'details': [
        ('Blood type:', 'Blood type here'),
        ('Allergies:', 'List of Allergies'),
        ('Other information:', 'Conditions and/or additional information'),
    ],
    'contacts': [
        ('Contact D:', 'Contact D phone number'),
        ('Contact E:', 'Contact E phone number'),
        ('Contact F:', 'Contact F phone number'),
    ],
    'shameless': [
        ("Hayley Denbraver is looking for her next opportunity",),
        ("Hire her for Developer Advocacy, Technical Content Writing, or Python Development",),
        ('Contact her @hayleydenb on Twitter, or find here at https://dev.to/hayleydenb or https://www.linkedin.com/in/hayleydenbraverpe),
    ],
}
ACCEPTED_NUMBERS = [TWIL_NUMBER, TWIL_EXAMPLE_NUMBER]

def main(req: func.HttpRequest) -> func.HttpResponse:
    
    # This determines what phone number is texting my twilio number and whether they are texting my sample or emergency number.
    # I am also getting the incoming text body, which will be used to properly respond. 
    send_to = req.params['From']
    send_from = req.params['To']
    incoming_message = req.params['Body'].lower()
    
    # These variables help construct the proper outgoing messages.
    is_sample = is_sample(req)
    emergency_info = SAMPLE_INFORMATION if is_sample else EMERGENCY_INFORMATION
    PIN = SAMPLE_PIN if is_sample else EMERGENCY_PIN
    body = incoming_message.strip().lower()

    # This logs incoming text. 
    logging.info(log_incoming_text(is_sample, send_to)

    # We run a security check to be sure of the following:
    # 1. That someone didn't set up a twilio number to hit my site.
    # 2. That the person texting my number is authorized to do so. We don't want to give health info to a 'wrong number'
    #
    # Depending on the result of the security check, the appropriate texts are kicked off. 
    security_check_and_workflow(send_to, send_from, incoming_message, is_sample)



def is_sample(req):
    which_number = req.params.get['To']
    if which_number == TWIL_EXAMPLE_NUMBER:
        return True
    elif which_number == TWIL_NUMBER:
        return False
    else:
        return None
    
def log_incoming_text(is_sample, send_to):
    sample_or_emergency = 'Sample' if is_sample else 'Emergency'
    return f'{sample_or_emergency} information was requested from {send_to}'

def security_check_and_workflow(send_to, send_from, incoming_message, is_sample):
    
    if is_sample == None:
        logging.info(f"Request was sent to an unauthorized number {send_to}")
        return func.HttpResponse(f"The request was sent to an unauthorized number")

    if body == PIN:
        send_initial_text(req, send_to, send_from, is_sample)
    
    else:
        messages = client.messages.list(
            from_=send_to,
            body=PIN
        )
        if messages:
            send_follow_up_text(req, send_to, send_from, incoming_message)
        
        else:
            return func.HttpResponse(f"See ID for instructions on texting")

def send_initial_text(req, send_to, send_from, is_sample):
    outgoing_message = f"""You have requested {NAME}'s emergency information.
        - Text 'contacts' for {NAME}'s emergency contacts
        - Text 'meds' for a list of {NAME}'s medications
        - Text 'details' for information like blood type, known conditions, etc.""" 

    if is_sample:
        outgoing_message = outgoing_message + "\n- Text 'shameless' for details on how to hire Hayley."
    
    send_message(outgoing_message, send_to, send_from)

def send_follow_up_text(req, send_to, send_from, incoming_message, emergency_info, is_sample):
    if incoming_message in emergency_info.keys():
        info_to_send = emergency_info[incoming_message]
        message = generate_message_from_emergency_info()
    else:
        send_initial_text(req, send_to, send_from, is_sample)

def send_message(body, send_to, send_from);
    message = client.messages.create(
        body=outgoing_message,
        from_=send_from,
        to=send_to,
        )


    