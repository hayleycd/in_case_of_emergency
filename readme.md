![Header image with title, "In Case of Emergency"](https://raw.githubusercontent.com/hayleycd/in_case_of_emergency/master/pictures/cover.png
)
>**_Everyone_ should make sure that their emergency contact information and important medical details are up to date and accessible in an emergency (AKA right now).**

# My application

Introducing _In Case of Emergency_, the Twilio app that makes it easy to keep emergency contact information up to date! I can also customize my information, making sure not to leave out anything

## License
This project is licensed under the MIT License. License text can be found [here](https://github.com/hayleycd/in_case_of_emergency/blob/master/license.md)

## Try it out!
I want to share the project with the DEV community, but I _do not_ want y'all to have access to my medical details or my emergency contacts. Boundaries are healthy. :wink:

But you don't have to take my word for it that the project works. I have set up a sample phone number and PIN (distinct from my actual emergency number and PIN) that is tied to data that is not personal. You can text the sample number yourself and see how the tool works. 

__1. Text '12358' to 1-206-312-4357. If you don't send this code to the number, all it will do is instruct you to follow directions on the ID.__

__2. Text 'meds', 'contacts', 'details', or 'shameless' to get further information.__

>__Texting 'shameless' will give you information on how to connect with me. I am currently on the job market for a Developer Advocate role and if you like my style, let's connect.__ 

This is what will show up on your phone when you follow the above instructions! 

![Screenshot of my phone utilizing the texting app. I sent the pin and got instructions back on how to navigate the information.](https://dev-to-uploads.s3.amazonaws.com/i/kxb0250256a65zwe23vh.jpg)

## Technologies

My application uses the following:
- A [Twilio account](https://www.twilio.com/try-twilio/?utm_campaign=ahoy-from-hayley-denbraver) and a paid Twilio [phone number](https://www.twilio.com/sms/?utm_campaign=ahoy-from-hayley-denbraver) set up to receive SMS messages
- An [Azure account](https://azure.microsoft.com/) and an [Azure Functions](https://azure.microsoft.com/en-us/services/functions/) app 
- [VS Code](https://code.visualstudio.com/) including the [Python](https://marketplace.visualstudio.com/items?itemName=ms-python.python) and [Azure Functions](https://marketplace.visualstudio.com/items?itemName=ms-azuretools.vscode-azurefunctions) extensions
- Twilio's [Python SDK](https://www.twilio.com/docs/libraries/python/?utm_campaign=ahoy-from-hayley-denbraver)
- I used [Black](https://github.com/psf/black) to format my python files. 

## Features

_In Case of Emergency_ provides the following via text to emergency personnel or a Good Samaritan who finds you in need:
- Medically relevant information(allergies, known conditions, blood type, anything that you personally would want a doctor to know in an emergency)
- Medications and any relevant dosing information
- Names and phone numbers of your emergency contacts 

Best of all, you can keep all of your information current by editing the relevant environment variables in Azure Functions. You can always add an item to your list of meds. You can remove an item from your medical details when it is no longer relevant (for instance: pregnancy, injury, ). Add and edit contacts with ease.  

## Get your own
Could you use something like this in your life? You can get your own. You will need:

1. An Azure account.
2. A Twilio account and a Twilio phone number.
3. To clone my [GitHub repository](https://github.com/hayleycd/in_case_of_emergency) and make any changes to the code to suit your situation.

### Steps to success with Azure

- Sign up for your free [Azure account](https://azure.microsoft.com/). You will get some credit to try it out for a month. 
- Download [VS Code](https://code.visualstudio.com/) and the [Python](https://marketplace.visualstudio.com/items?itemName=ms-python.python) and [Azure Functions](https://marketplace.visualstudio.com/items?itemName=ms-azuretools.vscode-azurefunctions) extensions.

![The screenshot shows what it looks like to find the Azure function extension in VS Code.](https://raw.githubusercontent.com/hayleycd/in_case_of_emergency/master/pictures/detectsazure.png)

- Authenticate your Azure account in VS Code. Once you have installed the Azure Functions extension, you should see a notification that will help you through the process. Now your VS Code install and your Azure account are connected. 
- Create a new Azure Function App through the Azure Portal in your webbrowser. 
- The defaults should be sufficient, though check your region.
- Once you feel good abou the settings, deploy! Azure will take a minute to deploy your app. 
- In VS Code, open the file containing the repository that you cloned and pulled down from my GitHub. VS Code should detect that you have a Azure function application. Follow any prompts that it may give you. 

![The Azure Function extension will detect when have opened a folder that has an Azure Function application.](https://raw.githubusercontent.com/hayleycd/in_case_of_emergency/master/pictures/detectsfunction.png)

- 


### Twilio account and phone number
Once you have a [Twilio account](https://www.twilio.com/try-twilio/?utm_campaign=ahoy-from-hayley-denbraver), you need to purchase and set up a Twilio phone number. 

You will want your phone number to behave in a certain way when someone texts you. Here is what it looks like to set it up:

![Screenshot of the Twilio phone number UI. When the number is sent a message, a GET request is made to my Azure function endpoint.](https://raw.githubusercontent.com/hayleycd/in_case_of_emergency/master/pictures/twiliophone.png)

When the number is sent a message, a GET request is made to my Azure function endpoint. I have obscured my URL, but if you want your own you can find yours in your Azure Function UI as shown:

![Screenshot indicates where to locate the url](https://raw.githubusercontent.com/hayleycd/in_case_of_emergency/master/pictures/get_url.png) 


### Environment variables
Once you have the basic set up in Azure and Twilio, you will need to populate your environment variables. When you are viewing your Azure Functions application in your Azure Portal, you will be able to configure your function (add environment variables). The link to that functionality is circled in the picture below. I have also circled where you can monitor your function. This will be particularly useful to troubleshoot any issues you may have with the environment variables, etc. 

![Image shows circled link to monitor the function and to configure the function's environment variables.](https://raw.githubusercontent.com/hayleycd/in_case_of_emergency/master/pictures/configandmore.png)
 
The image below shows what you will find when you are configuring your function. The variables that are not circled come pre-populated. 

![Image shows all the environment variables that you will need for this project.](https://raw.githubusercontent.com/hayleycd/in_case_of_emergency/master/pictures/configuration.png) 

You can add and edit variables by clicking the links indicated by the arrows in your configuration UI. Variables indicated in red should be found in your Twilio account (AUTH_TOKEN and ACCOUNT_SID) and are necessary to use the Twilio API. The variables indicated in blue you will need to create, and include things like your Twilio number, etc.

The trickiest environment variable is EMERGENCY_INFORMATION. It can be long and, if not formatted properly, can be a problem. It must be in JSON format. Don't add a single quote to the outside of the structure. _Only_ use double quotes, JSON doesn't understand single quotes. You can take the template below and populate it with your information. 

    {
    "meds": [
        ["Med A: ", "Notes for A"], 
        ["Med B: ", "Notes for B"]
        ],
    "details":[
        ["Blood type: ", "Blood Type"], 
        ["Allergies: ", "Allergies"], 
        ["Other information: ", "Other health information"]
        ], 
    "contacts": [
        ["Contact 1", "Contact 1 number"],
        ["Contact 2", "Contact 2 number"]
        ]
    }

When you are done adding variables, you will need to save them before they will be applied to your function. 

### Let me know!

If you give the above a try, please let me know. I would love to hear from you and can be contacted most readily on [Twitter](twitter.com/hayleydenb).

## A parting word on security

Some real talk--this application strikes a balance between making sure information is accessible in an emergency and risking exposure of private information. I have done a number of things to protect my privacy, but if you spin up your own version, you need to consider what you are comfortable with. 

Here are a few security steps I took in building this project:

1. The Twilio number associated with my ID has not been published on dev.to and it was _never_ checked into my version control. You don't publish your keys in git, don't put your phone number in there either, even at the beginning. If you put important information like this in git, people can browse the history and find it, even if you later remove it. 

2. I did not hard code any of my medicines, medical history, or my emergency contacts. Again, you want someone to be able to access it in an emergency, but you don't want to publish your personal business for the whole internet to see. 

3. I included a PIN on my ID. My ID will instruct someone to text my Twilio number with my PIN to initiate the exchange. If a number has sent the PIN, it can navigate the options. If it has not, it only will get a message saying to check the ID for instructions. This protects me from someone accidentally texting me and stumbling on my medical history. 

4. My Twilio account and my Azure account are protected by [2FA](https://authy.com/what-is-2fa/). This helps protect my environment variables including: my Twilio phone number, my PIN, my emergency contacts, my personal medical information as well as the logs present in both my Twilio and Azure accounts. 

5. I have limited the phone numbers that can hit my function and have not published the full URL. That means that if you somehow had the correct URL, you would be unable to set up a Twilio number to hit it and get my medical information.  

6. I am only working with my own information and have weighed the pros and cons. Additionally, I gained consent from my emergency contacts to include their phone numbers in this endeavor. One of my emergency contacts is also an experienced developer and we did a code review in order to get another pair of eyes on it. 

# Final thoughts
Thanks to Twilio and the DEV community for hosting this hackathon. I would love for this project to be considered for either the COVID communications or the X-factor category.

And to the DEV community, please be safe and well whether you are coding, sewing masks, taking care of loved ones, playing Animal Crossing, baking bread, or any or all of the above. Remember to take breaks and be kind to yourselves. This too, shall pass.