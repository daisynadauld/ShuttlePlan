import base64
from email_processor import EmailProcessor
#from drive import DriveAPI
from event_creator import EventCreator

"""First step is to extract emails and get the emails/information we are interested in"""

email_processer = EmailProcessor()

booking_emails = email_processer.start_process()
data = email_processer.set_data_dict(booking_emails)
data_dict = email_processer.get_data_dict()

print(data_dict)

for i in data_dict:
    event_data = data_dict[i]
          
    """The Second step is to create a new calendar event for each booking with details from the email"""

    event_creator = EventCreator()
    calendar_service = event_creator.start_process()
    event_creator.create_booking_event(calendar_service, event_data)

"""The last step is to create a folder in Google Drive with the client's name/service date and fill 
it with client information"""
    # Create a new folder in Google Drive
    #folder_id = drive_api.create_folder(email_sender)
