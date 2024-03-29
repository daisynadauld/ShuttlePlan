# google_calendar.py
from __future__ import print_function

import os.path

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

# If modifying these scopes, delete the file token.json.
SCOPES = ['https://www.googleapis.com/auth/calendar']

class CalendarAPI:
    def __init__(self):
        self

    def get_credentials(self):
        creds = None
        # The file token.json stores the user's access and refresh tokens, and is
        # created automatically when the authorization flow completes for the first
        # time.
        if os.path.exists('calendartoken.json'):
            creds = Credentials.from_authorized_user_file('calendartoken.json', SCOPES)
        # If there are no (valid) credentials available, let the user log in.
        if not creds or not creds.valid:
            if creds and creds.expired and creds.refresh_token:
                creds.refresh(Request())
            else:
                flow = InstalledAppFlow.from_client_secrets_file(
                    'credentials.json', SCOPES)
                creds = flow.run_local_server(port=0)
            # Save the credentials for the next run
            with open('calendartoken.json', 'w') as token:
                token.write(creds.to_json())

        return creds

    def build_calendar(self):
        """Opens up Calendar and does the authentication."""
        creds = self.get_credentials()

        try:
            # Call the Calendar API
            service = build('calendar', 'v3', credentials=creds)
            return service
        except:
            print("Error: Could not build calendar")
            exit()