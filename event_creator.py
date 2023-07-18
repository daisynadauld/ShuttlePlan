# event_creator.py
import json
from google_calendar import CalendarAPI
import datetime
import dateparser

#calendarId='c_6c6cba9f30a55304661d94debd330c8f7cf111d69c777f332b795e75acb36fc9@group.calendar.google.com'

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

    def format_dates(self, date_str):
        #This will format the date to be usable for google calendar despite how the clients write it
        parsed_date = dateparser.parse(date_str)
        if parsed_date:
            formatted_date = parsed_date.strftime("%Y-%m-%d")
            return formatted_date
        else:            
            print(f"This date was not parsed: ")
            print(date_str)
            return None  # Return None if the date parsing fails
        
    def format_info(self, event_data):
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
        return event_description

    def create_booking_event(self, service,  event_data):
        # Implement the logic to create a Google Calendar event
        # Use the service object to interact with the API
        # Pass the event data as a parameter to create the event
        event_title = event_data[14] + event_data[0]

        date_parts = event_data[15].split(" ", 4)
        formatted_date = " ".join(date_parts[:-1])
        start_date = self.format_dates(formatted_date)

        end_date_original = self.format_dates(event_data[12])

        if end_date_original == None:
            print("Bad end date")
            event_description = self.format_info(event_data)
            with open("bookings_that_need_manual_addition.txt", "a") as file:
                # Write data to the file
                file.write(event_description)
                file.write("\n")
                file.write("\n")
            return

        # We must format the end date
        date = datetime.datetime.strptime(end_date_original, "%Y-%m-%d")
        end_date = date.strftime("%Y-%m-%d")

        if start_date == None or end_date < start_date:
            print("Some date issue")
            event_description = self.format_info(event_data)
            with open("bookings_that_need_manual_addition.txt", "a") as file:
                # Write data to the file
                file.write(event_description)
                file.write("                                                                      ")
            return
        else:
            event_description = self.format_info(event_data)

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
            events = service.events().list(calendarId='daisykunzler@gmail.com', q=event_title).execute()
            existing_events = events.get('items', [])

            if existing_events:
                print("Event already exists on the calendar. Skipping creation.")
                return
            else:
                # Insert the event into the calendar
                try:
                    service.events().insert(calendarId='daisykunzler@gmail.com', body=event).execute()
                except:
                    print("Error while trying to add booking to calendar.")
                    print("Event with issue: ")
                    with open("bookings_that_need_manual_addition.json", "a") as file:
                        json.dump(event_data, file)
                    print("Event added to bookings that need manual addition file")
                    return


    def get_events(self, service, time_min=None, time_max=None):
        # Get the current date
        current_date = datetime.datetime.now().date().isoformat()

        # Set the default value for time_min if not provided
        if not time_min:
            time_min = current_date

        # Fetch events from the calendar starting from the specified time_min and up to the specified time_max
        calendarId = "daisykunzler@gmail.com"
        events_list_params = {
            'calendarId': calendarId,
            'timeMin': time_min,
            'timeMax': time_max if time_max else None
        }
        events = service.events().list(**events_list_params).execute()
        existing_events = events.get('items', [])

        event_dict = {}  # Dictionary to store event titles as keys and start/end dates as values

        # Iterate through existing events and extract title, start, and end dates
        for event in existing_events:
            event_title = event.get('summary')
            event_start_date = event['start'].get('date')
            event_end_date = event['end'].get('date')

            if event_start_date == None and event_end_date == None:
                pass
            else:
                # Store the start and end dates as values in the dictionary
                event_dict[event_title] = {
                    'start_date': event_start_date,
                    'end_date': event_end_date
                }

        # Return the dictionary of event titles with start and end dates
        print("Event Dict: ")
        print(event_dict)
        overlapping_events = self.get_overlapping_events(event_dict)
        print("Overlapping Events: ")
        print(overlapping_events)
        print()
        for i in overlapping_events:
            print()
            print(i)

        return overlapping_events
    
    def get_overlapping_events(self, existing_events):
        overlapping_groups = []

        events = list(existing_events.items())
        grouped_events = set()  # Track the events already grouped

        for i, (title1, event1) in enumerate(events):
            if tuple(event1.items()) in grouped_events:
                continue  # Skip if the event is already grouped

            overlapping_group = [(title1, event1)]

            for j, (title2, event2) in enumerate(events[i+1:], start=i+1):
                if event1['end_date'] > event2['start_date'] and event1['start_date'] < event2['end_date']:
                    overlapping_group.append((title2, event2))
                    grouped_events.add(tuple(event2.items()))

            if len(overlapping_group) > 1:
                overlapping_groups.append(overlapping_group)

        return overlapping_groups

    from datetime import datetime, timedelta

    def find_most_overlapping_date(self, event_tuples):
        if len(event_tuples) == 1:
            start_date = event_tuples[0][1]['start_date']  # Return the start date if there is only one item
            return (datetime.datetime.strptime(start_date, "%Y-%m-%d") + datetime.timedelta(days=1)).strftime("%Y-%m-%d")
        elif len(event_tuples) == 0:
            return


        # Step 2: Extract the start and end dates as datetime objects
        start_dates = [datetime.datetime.strptime(event[1]['start_date'], "%Y-%m-%d") for event in event_tuples]
        end_dates = [datetime.datetime.strptime(event[1]['end_date'], "%Y-%m-%d") for event in event_tuples]

        # Step 3: Create a dictionary to track overlapping dates
        overlap_counts = {}

        # Step 4: Iterate over the list and check for overlaps
        for i in range(len(event_tuples)):
            for j in range(i + 1, len(event_tuples)):
                # Step 5: Check for overlaps and increment the count
                if start_dates[i] <= end_dates[j] and start_dates[j] <= end_dates[i]:
                    overlap_dates = set(
                        range((max(start_dates[i], start_dates[j]) - min(start_dates[i], start_dates[j])).days + 1)
                    )
                    for date in overlap_dates:
                        overlap_counts[date] = overlap_counts.get(date, 0) + 1

        if not overlap_counts:
            return None

        # Step 6: Find the date(s) with the maximum count
        max_count = max(overlap_counts.values())
        max_dates = [start_dates[0] + datetime.timedelta(days=date) for date, count in overlap_counts.items() if count == max_count]

        if max_count == 0:
            return None  # No overlapping dates found

        if len(max_dates) == 1:
            return max_dates[0].strftime("%Y-%m-%d")  # Return the single max date if there is no tie

        # Step 7: Remove tuples that include max_dates between their start and end date
        event_tuples = [
            event for event in event_tuples if not datetime.datetime.strptime(event[1]['start_date'], "%Y-%m-%d") <= max_dates[0] <= datetime.datetime.strptime(event[1]['end_date'], "%Y-%m-%d")
        ]

        # Recursively find the most overlapping date in the updated subset
        return self.find_most_overlapping_date(event_tuples)
    
    def calc_drives(self, overlapping_groups):
        main_events = []
        middle_events = []

        for group in overlapping_groups:
            main_group = []
            middle_group = []

            for event in group:
                event_title = event[0]
                event_dates = event[1]

                # Check the event title and add it to the appropriate group
                if 'main' in event_title.lower():
                    main_group.append((event_title, event_dates))
                elif 'middle' in event_title.lower():
                    middle_group.append((event_title, event_dates))

            if main_group:
                main_events.append(main_group)

            if middle_group:
                middle_events.append(middle_group)

        main_overlap_dates = []
        middle_overlap_dates = []

        for main_group in main_events:
            main_overlap_date = self.find_most_overlapping_date(main_group)
            if main_overlap_date:
                main_overlap_dates.append(main_overlap_date)

        for middle_group in middle_events:
            middle_overlap_date = self.find_most_overlapping_date(middle_group)
            if middle_overlap_date:
                middle_overlap_dates.append(middle_overlap_date)

        # Sort the overlapping dates in ascending order
        main_overlap_dates.sort()
        middle_overlap_dates.sort()

        # Calculate the best date for each type of event
        main_date = main_overlap_dates[0] if main_overlap_dates else None
        middle_date = middle_overlap_dates[0] if middle_overlap_dates else None

        # Determine the next day for middle events if main events are present
        if main_date and middle_date and main_date <= middle_date:
            middle_date = (datetime.datetime.strptime(middle_date, "%Y-%m-%d") + datetime.timedelta(days=1)).strftime("%Y-%m-%d")

        return main_overlap_dates, middle_overlap_dates
    
    def make_drive_events(self, calendar_service, main_dates, middle_dates):
        # Create events for middle dates
        for date in middle_dates:
            event = {
                'summary': 'Middle Drive',
                'start': {
                    'date': date,
                    'timeZone': 'America/Denver'
                },
                'end': {
                    'date': date,
                    'timeZone': 'America/Denver'
                },
                'reminders': {
                    'useDefault': False
                },
                'colorId': '5',  # Set color to banana (yellow)
            }

            # Insert the event into the calendar
            try:
                calendar_service.events().insert(calendarId='daisykunzler@gmail.com', body=event).execute()
                print(f"Middle Drive event created on {date}")
            except Exception as e:
                print(f"Error creating Middle Drive event on {date}: {str(e)}")

        # Create events for main dates
        for date in main_dates:
            event = {
                'summary': 'Main Drive',
                'start': {
                    'date': date,
                    'timeZone': 'America/Denver'
                },
                'end': {
                    'date': date,
                    'timeZone': 'America/Denver'
                },
                'reminders': {
                    'useDefault': False
                },
                'colorId': '11',  # Set color to tangerine (orange)
            }

            # Insert the event into the calendar
            try:
                calendar_service.events().insert(calendarId='daisykunzler@gmail.com', body=event).execute()
                print(f"Main Drive event created on {date}")
            except Exception as e:
                print(f"Error creating Main Drive event on {date}: {str(e)}")



'''
    def calc_drives(self, overlapping_groups):
        main_events = []
        middle_events = []

        for group in overlapping_groups:
            main_group = []
            middle_group = []

            for event in group:
                event_title = event[0]
                event_start_date = event[1]['start_date']
                event_end_date = event[1]['end_date']

                # Check the event title and add it to the appropriate group
                if 'main' in event_title.lower():
                    main_group.append((event_title, {'start_date': event_start_date, 'end_date': event_end_date}))
                elif 'middle' in event_title.lower():
                    middle_group.append((event_title, {'start_date': event_start_date, 'end_date': event_end_date}))

            if main_group:
                main_events.append(main_group)

            if middle_group:
                middle_events.append(middle_group)

        main_overlap_dates = []
        middle_overlap_dates = []

        for main_group in main_events:
            main_overlap_dates.append(self.find_most_overlapping_date(main_group))

        for middle_group in middle_events:
            middle_overlap_dates.append(self.find_most_overlapping_date(middle_group))

        return {
            'Main': main_overlap_dates,
            'Middle': middle_overlap_dates
        }
        '''

'''
    def calc_drives(self, overlapping_groups):
        #events are preferably to start the day after the start date for the exisiting event, if there are two or more events, then do the earliest overlap date for the events, but we dont want the event to start on the end date or later of any of the events
        #if no events overlap, make a day long event for each event, the day after start date
        #If events overlap, and they have the same title, then make a single event the day after the later events start date, unless it is the end date or later of the first event, then make the event the second events start date
        #If events overlap, and have different titles, make more if statements based off of the title names, if the titles are "main" and "middle", make an event
        #If events are one day apart, and there is a main before a middle, then make an event for them
        #If events are one day apart and there is a middle before a main, then you need to make seperate events
        #If there are half day trips, they can be added to either mains or middles
        #turn the corner will be its own thing
        for event in event_dict:
            if event["start date"]
        for key in event_dict:
            if key has main
            elif key has middle
            elif key has stanley to salmon
            elif key has marsh to cache 
            elif key has
        overlap_dates = []

        for group in overlapping_groups:

            # Step 1: Convert the data into a list of tuples
            event_tuples = [(event[0], event[1]['start_date'], event[1]['end_date']) for event in group]
            most_overlapping_date = self.find_most_overlapping_date(group)

            overlap_dates.append(most_overlapping_date)


            
            #if the earliest start date
            #latest end date 
            print ("this is here")
            print(group)
            # Get the start and end dates for all events in the group
            event_dates = [event[1]['start_date'] for event in group]

            # Find the earliest start date and latest end date in the group
            earliest_start_date = min(event_dates)
            latest_end_date = max(event[1]['end_date'] for event in group)

            # Calculate the overlap date
            overlap_date = datetime.datetime.strptime(earliest_start_date, "%Y-%m-%d")
            while overlap_date <= datetime.datetime.strptime(latest_end_date, "%Y-%m-%d"):
                if all(
                    datetime.datetime.strptime(event[1]['start_date'], "%Y-%m-%d") <= overlap_date <=
                    datetime.datetime.strptime(event[1]['end_date'], "%Y-%m-%d")
                    for event in group
                ):
                    overlap_dates.append(overlap_date.strftime("%Y-%m-%d"))
                    break
                overlap_date += datetime.timedelta(days=1)


            print()
            print(overlap_dates)
            return 
'''
