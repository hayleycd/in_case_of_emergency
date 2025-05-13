---
layout: page
title: Event flow
permalink: /event-flow/
---

{: .note }
This project is no longer deployed. It is now only a writing and code sample. You will not be able to text the sample line. 

## Event flow

This is a step by step peek into how the _In Case of Emergency_ app works. 

1. User finds ID with phone number and PIN. 
2. User texts PIN to phone number. 
3. Incoming text to Twilio number triggers a webhook that makes a GET request to the Azure function app, triggering the [`emergency_contact`](https://github.com/hayleycd/in_case_of_emergency/blob/master/emergency_contact/__init__.py) function. 
4. The `emergency_contact` function executes the following steps. 

- Checks to see if the Twilio number texted was my sample line, my actual emergency line, or another number. If it is another number, an error is thrown and further information won't be sent via SMS.
- If the incoming message matches the PIN, a text that explains how to get further information is sent.
- If the incoming message is not the PIN, the function checks twilio message history to see if the sender's phone number has sent the PIN.
- If the sender has not sent the PIN, they receive a message asking them to send the PIN.
- If they have sent the PIN, the function determines what message to send.
- The incoming message is cleaned up, extraneous spaces are removed and message is converted to all lower case.
- If the incoming message was one of the keys ("contacts", "meds", "details"...) it generates and sends a text based on the information requested.
- If the incoming message is not one of the keys, the initial text that explains how to request information is sent.
- Once a message is sent, a 200 status is returned to indicate the function executed. 
