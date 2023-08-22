---
layout: page
title: Security
permalink: /security/
nav_order: 5
---

{: .note }
This project is no longer deployed. It is now only a writing and code sample. You will not be able to text the sample line. 

## A parting word on security

Some real talk--this application strikes a balance between making sure information is accessible in an emergency and risking exposure of private information. I have done a number of things to protect my privacy, but if you spin up your own version, you need to consider what you are comfortable with. 

Here are a few security steps I took in building this project:

1. The Twilio number associated with my ID has not been published on dev.to and it was _never_ checked into my version control. You don't publish your keys in git, don't put your phone number in there either, even at the beginning. If you put important information like this in git, people can browse the history and find it, even if you later remove it. 

2. I did not hard code any of my medicines, medical history, or my emergency contacts. Again, you want someone to be able to access it in an emergency, but you don't want to publish your personal business for the whole internet to see. 

3. I included a PIN on my ID. My ID will instruct someone to text my Twilio number with my PIN to initiate the exchange. If a number has sent the PIN, it can navigate the options. If it has not, it only will get a message saying to check the ID for instructions. This protects me from someone accidentally texting me and stumbling on my medical history. 

4. My Twilio account and my Azure account are protected by [2FA](https://authy.com/what-is-2fa/). This helps protect my environment variables including: my Twilio phone number, my PIN, my emergency contacts, my personal medical information as well as the logs present in both my Twilio and Azure accounts. 

5. I have limited the phone numbers that can hit my function and have not published the full URL. That means that if you somehow had the correct URL, you would be unable to set up a Twilio number to hit it and get my medical information.  

6. I am only working with my own information and have weighed the pros and cons. Additionally, I gained consent from my emergency contacts to include their phone numbers in this endeavor. One of my emergency contacts is also an experienced developer and we did a code review in order to get another pair of eyes on it.
