# event_creator.py
from google_calendar import CalendarAPI
import datetime

class EventCreator:
    def __init__(self):
        self

    def start_process(self):
        # Create instance of the API module
        calendar_api = CalendarAPI()
        # Build the calendar service
        calendar_service = calendar_api.build_calendar()
        # Fetch email details
        return calendar_service

    def format_dates(self, event_data):
        #This will format the date to be usable for google calendar despite how the clients write it
        format_mapping = {
            "%A, %B %d, %Y": lambda d: d.strftime("%Y-%m-%d"),  # Monday, June 5, 2023 8:00 AM MDT
            "%B %d, %Y": lambda d: d.strftime("%Y-%m-%d"),  # June 10, 2023
            "%B %dth, %Y": lambda d: d.strftime("%Y-%m-%d"),  # 'June 10th, 2023
            "%B %d": lambda d: d.strftime("%Y-%m-%d"),  # June 10
            "%dth %B %Y": lambda d: d.strftime("%Y-%m-%d"),  # 10th June 2023
            "%dth %B": lambda d: d.strftime("%Y-%m-%d"),  # 10th June
            "%m/%d/%Y": lambda d: d.strftime("%Y-%m-%d"),  # 06/10/2023
            "%d/%m/%Y": lambda d: d.strftime("%Y-%m-%d"),  # 10/06/2023
            "%Y-%m-%d": lambda d: d.strftime("%Y-%m-%d"),  # 2023-06-10
            "%drd %B %Y": lambda d: d.strftime("%Y-%m-%d"),  # 23rd June 2023
            "%B %d, '%y": lambda d: d.strftime("%Y-%m-%d"),  # June 10, '23
            "%d-%b-%Y": lambda d: d.strftime("%Y-%m-%d"),  # 10-Jun-2023
            "%d-%b": lambda d: d.strftime("%Y-%m-%d"),  # 10-Jun
            "%B %d": lambda d: d.strftime("%Y-%m-%d"),  # June 10
            "June %d, %Y": lambda d: d.strftime("%Y-%m-%d"),  # June 10, 2023
            "June %d": lambda d: d.strftime("%Y-%m-%d"),  # June 10
            "%dth of June, %Y": lambda d: d.strftime("%Y-%m-%d"),  # 10th of June, 2023
            "%dth of June": lambda d: d.strftime("%Y-%m-%d"),  # 10th of June
            "June %d, '%y": lambda d: d.strftime("%Y-%m-%d"),  # June 10, '23
            "June %d '%y": lambda d: d.strftime("%Y-%m-%d"),  # June 10 '23
            "%d-%b-%y": lambda d: d.strftime("%Y-%m-%d"),  # 10-Jun-23
            "%d-%b-%Y": lambda d: d.strftime("%Y-%m-%d"),  # 10-Jun-2023
            "%dth": lambda d: d.strftime("%Y-%m-%d"),  # 10th
            "%d": lambda d: d.strftime("%Y-%m-%d")  # 10
        }

        for date_format, conversion_func in format_mapping.items():
            try:
                date_object = datetime.datetime.strptime(event_data, date_format).replace(year=datetime.datetime.today().year)
                return conversion_func(date_object)
            except ValueError:
                continue

        return None  # Return None if the input format is not recognized

    def create_booking_event(self, service,  event_data):
        # Implement the logic to create a Google Calendar event
        # Use the service object to interact with the API
        # Pass the event data as a parameter to create the event
        event_title = event_data[14] + event_data[0]

        date_parts = event_data[15].split(" ", 4)
        formatted_date = " ".join(date_parts[:-1])
        start_date = self.format_dates(formatted_date)

        event_description = (
            event_data[0] + "\n" +
            "Email: " + event_data[1] + "\n" +
            "Number: " + event_data[2] + "\n" +
            "Emergency Contact: " + event_data[3] + " (" + event_data[4] + ")\n" +
            "Number: " + event_data[5] + "\n" +
            "Vehicle Information: " + event_data[9] + " " + event_data[6] + " " + event_data[7] +
            " " + event_data[8] + "\n" + 
            "Description: " + event_data[10] + "\n" +
            "Key Location: " + event_data[11]
            )
        

        end_date_original = self.format_dates(event_data[12])
        # We must add one day to the date to make it show correctly on the calendar
        date = datetime.datetime.strptime(end_date_original, "%Y-%m-%d")
        next_day = date + datetime.timedelta(days=1)
        end_date = next_day.strftime("%Y-%m-%d")

        event = {
        'summary': event_title,
        'description': event_description,
        'start': {
            'date': start_date,
            'timeZone': 'America/Denver',  # e.g., 'America/New_York'
        },
        'end': {
            'date': end_date,
            'timeZone': 'America/Denver',  # e.g., 'America/New_York'
        },
        'reminders': {
            'useDefault': False,
        },
        'transparency': 'transparent',  # Set the event as transparent (all-day)
        }

        # Check if the event already exists on the calendar
        events = service.events().list(calendarId='primary', q=event_title).execute()
        existing_events = events.get('items', [])


        if existing_events:
            print("Event already exists on the calendar. Skipping creation.")
            return
        else:
            # Insert the event into the calendar
            service.events().insert(calendarId='primary', body=event).execute()

    # Implement other methods related to Calendar interactions, if required
