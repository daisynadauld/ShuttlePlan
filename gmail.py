from __future__ import print_function

import os.path

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

# If modifying these scopes, delete the file token.json.
SCOPES = ['https://mail.google.com/']

class GmailAPI:
    def __init__(self):
        self

    def get_credentials(self):
        creds = None
        # The file token.json stores the user's access and refresh tokens, and is
        # created automatically when the authorization flow completes for the first
        # time.
        if os.path.exists('gmailtoken.json'):
            creds = Credentials.from_authorized_user_file('gmailtoken.json', SCOPES)
        # If there are no (valid) credentials available, let the user log in.
        if not creds or not creds.valid:
            if creds and creds.expired and creds.refresh_token:
                creds.refresh(Request())
            else:
                flow = InstalledAppFlow.from_client_secrets_file(
                    'credentials.json', SCOPES)
                creds = flow.run_local_server(port=0)
            # Save the credentials for the next run
            with open('gmailtoken.json', 'w') as token:
                token.write(creds.to_json())

        return creds

    def build_gmail(self):
        """Opens up Gmail and does the authentication."""
        creds = self.get_credentials()

        # Call the Gmail API
        service = build('gmail', 'v1', credentials=creds)
        return service

    def fetch_emails(self, service):
        # Extract and return a list of email objects
        LABEL_ID = 'INBOX'
        try:
            emails = service.users().messages().list(userId='me', labelIds=[LABEL_ID]).execute()
            messages = emails.get('messages', [])
        except HttpError:
            print('An error occurred while trying to fetch emails')

        return messages