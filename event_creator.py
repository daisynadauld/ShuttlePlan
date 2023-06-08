# event_creator.py
from googleapiclient.discovery import build

class EventCreator:
    def __init__(self, credentials):
        self.service = build('calendar', 'v3', credentials=credentials)

    def create_event(self, event_data):
        # Implement the logic to create a Google Calendar event
        # Use the self.service object to interact with the API
        # Pass the event_data as a parameter to create the event

        event = self.service.events().insert(calendarId='primary', body=event_data).execute()
        event_id = event.get('id')

        return event_id

    # Implement other methods related to event interactions, if required
