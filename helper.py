import logging
import os
import json

import azure.functions as func
from twilio.rest import Client

# Environment variables

ACCOUNT_SID = os.environ["ACCOUNT_SID"]
AUTH_TOKEN = os.environ["AUTH_TOKEN"]
TWIL_NUMBER = os.environ["TWIL_NUMBER"]
TWIL_EXAMPLE_NUMBER = os.environ["TWIL_EXAMPLE_NUMBER"]
EMERGENCY_PIN = os.environ["EMERGENCY_PIN"]
SAMPLE_PIN = os.environ["SAMPLE_PIN"]
EMERGENCY_INFORMATION = json.loads(os.environ["EMERGENCY_INFORMATION"])
NAME = os.environ["NAME"]

# Global variables

CLIENT = Client(ACCOUNT_SID, AUTH_TOKEN)
SAMPLE_INFORMATION = {
    "meds": [
        ("Med A: ", "Notes for A"),
        ("Med B: ", "Notes for B"),
        ("Med C: ", "Notes for C"),
    ],
    "details": [
        ("Blood type: ", "Blood type here"),
        ("Allergies: ", "List of Allergies"),
        ("Other information: ", "Conditions and/or additional information"),
    ],
    "contacts": [
        ("Contact D: ", "Contact D phone number"),
        ("Contact E: ", "Contact E phone number"),
        ("Contact F: ", "Contact F phone number"),
    ],
    "shameless": [
        ("Hayley Denbraver is looking for her next opportunity.", ""),
        (
            "Hire her for Developer Advocacy, Technical Content Writing, or Python Development.",
            "",
        ),
        (
            "Contact her @hayleydenb on Twitter, or at hayley.denbraver@gmail.com",
            "",
        ),
    ],
    "error": [
        ("Let me trigger an error for you. Check Sentry!", ""),
    ],
}

def is_sample(send_from):
    if send_from == TWIL_EXAMPLE_NUMBER:
        return True
    elif send_from == TWIL_NUMBER:
        return False
    else:
        return None

def log_incoming_text(is_sample, send_to):
    sample_or_emergency = "Sample" if is_sample else "Emergency"
    return f"{sample_or_emergency} information was requested from {send_to}"

def security_check_and_workflow(
    PIN, send_to, send_from, incoming_message, is_sample, emergency_info
):

    if is_sample == None:
        logging.info(f"Request was sent to an unauthorized number {send_from}")
        return func.HttpResponse("Forbidden", status_code=403)

    if incoming_message.strip() == PIN:
        send_initial_text(send_to, send_from, is_sample)

    else:
        messages = CLIENT.messages.list(from_=send_to, to=send_from)
        sent_pin = False
        for message in messages:
            if message.body.strip() == PIN:
                sent_pin = True
        if sent_pin:
            send_follow_up_text(send_to, send_from, incoming_message, emergency_info)

        else:
            send_message("See ID for instructions", send_to, send_from)

def send_initial_text(send_to, send_from, is_sample):
    outgoing_message = f"""You have requested {NAME}'s emergency information.
    - Text 'contacts' for {NAME}'s emergency contacts.
        
    - Text 'meds' for a list of {NAME}'s medications.
        
    - Text 'details' for information like blood type, known conditions, etc."""

    if is_sample:
        outgoing_message = (
            outgoing_message
            + "\n\n- Text 'shameless' for details on how to hire Hayley."
            + "\n\n- Text 'error' to trigger an error"
        )

    send_message(outgoing_message, send_to, send_from)

def send_follow_up_text(send_to, send_from, incoming_message, emergency_info):
    if incoming_message in emergency_info.keys():
        info_to_send = emergency_info[incoming_message]
        message = generate_message_from_emergency_info(info_to_send)
        send_message(message, send_to, send_from)
        throw_an_error(incoming_message)
    else:
        send_initial_text(send_to, send_from, is_sample)

def send_message(outgoing_message, send_to, send_from):
    message = CLIENT.messages.create(
        body=outgoing_message, from_=send_from, to=send_to,
    )
    return func.HttpResponse(
        "You can text this number again if you need more information.", status_code=200
    )

def generate_message_from_emergency_info(info_to_send):
    outgoing_message = ""
    for each in info_to_send:
        outgoing_message = outgoing_message + each[0] + each[1] + "\n\n"
    return outgoing_message

def throw_an_error(incoming_message):
    if incoming_message == "error":
        1/0
