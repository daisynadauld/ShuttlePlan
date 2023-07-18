# ShuttlePlan
A Google API and Python application which will fetch details from client emails, add them to the company Google calendar, and then plan the best drives for the shuttle drivers.

Main Application File: Create a main file, such as main.py, which acts as the entry point for your application. This file will handle the initialization and coordination of other modules and classes.

Credentials: Store your API credentials securely. You can use a separate file, such as credentials.json, to store the client secrets, access tokens, or any other authentication information required by the APIs. Make sure this file is not publicly accessible.

Google Calendar Module:

calendar.py: Create a module to handle interactions with the Google Calendar API. This module should contain classes and functions related to fetching, creating, and updating calendar events. Use the official Google Calendar API documentation to guide your implementation.
Google Drive Module:

drive.py: Create a module to handle interactions with the Google Drive API. This module should contain classes and functions related to creating and managing folders in Google Drive. Refer to the official Google Drive API documentation for the necessary methods and endpoints.
Gmail Module:

gmail.py: Create a module to handle interactions with the Gmail API. This module should contain classes and functions to fetch details from emails, such as subject, sender, and body content. Use the official Gmail API documentation to understand how to retrieve email information.
Email Processing Module:

email_processor.py: Create a module responsible for processing emails and extracting relevant details. This module should use the Gmail module to fetch email data, extract necessary information, and return it for further processing.
Folder Creation Module:

folder_creator.py: Build a module to handle the creation of new folders in Google Drive. This module should use the Google Drive module to interact with the Drive API and create folders based on the extracted details from the emails.
Event Creation Module:

event_creator.py: Develop a module responsible for creating Google Calendar events. This module should use the Google Calendar module to interact with the Calendar API and generate new events based on the extracted email details and existing events on the calendar.
