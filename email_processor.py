# email_processor.py
import base64
from gmail import GmailAPI

class EmailProcessor:
    """Extract emails and get the detials from the emails we are interested in"""

    def __init__(self):
        self.data_dict = {}

    def start_process(self):
            # Create an instance of the API module
        gmail_api = GmailAPI()
        # Build the Gmail service
        gmail_service = gmail_api.build_gmail()

        # Fetch all email details
        emails = []
        page_token = None
        while True:
            results = gmail_service.users().messages().list(userId='me', pageToken=page_token).execute()
            messages = results.get('messages', [])
            emails.extend(messages)
            page_token = results.get('nextPageToken')
            if not page_token:
                break

        subject_of_interest = ['Fwd: You got a new booking!']
        booking_emails = []
        e_id = 0

        if not emails:
            print("No emails found.")
        else:
            for email in emails:
                # Extract relevant information from the email
                msg = gmail_service.users().messages().get(userId="me", id=email["id"]).execute()
                email_data = msg["payload"]["headers"]
                for values in email_data:
                    name = values["name"]
                    if name == "From":
                        from_name = values["value"]
                        # print(from_name)
                        subject = [j["value"] for j in email_data if j["name"] == "Subject"]

                # Get the body of the email
                try:
                    for p in msg["payload"]["parts"]:
                        if p["mimeType"] in ["text/plain"]:
                            data = base64.urlsafe_b64decode(p["body"]["data"]).decode("utf-8")
                except KeyError:
                    pass

                # Keep only the emails we are interested in
                if subject == subject_of_interest:
                    booking_emails.append(data)
                    e_id += 1
        return booking_emails
    
    def set_data_dict(self, booking_emails):
        # Here we assign information to variables for later use
        id = 0
        for booking_email in booking_emails:
            client_name = self.extract_information(booking_email, "Name: ", "Email: ")
            client_email = self.extract_information(booking_email, "Email: ", "Phone Number: ")
            client_phone_number = self.extract_information(booking_email, "Phone Number: ", "Number of Vehicles in your party: ")
            emergency_contact = self.extract_information(booking_email, "Emergency Contact Name: ", "Emergency Contact Relation: ")
            emergency_contact_relation = self.extract_information(booking_email, "Emergency Contact Relation: ", "Emergency Contact Phone Number: ")
            emergency_contact_number = self.extract_information(booking_email, "Emergency Contact Phone Number: ", "I authorize")
            vehicle_make = self.extract_information(booking_email, "Vehicle Make: ", "Vehicle Model: ")
            vehicle_model = self.extract_information(booking_email, "Vehicle Model: ", "License Plate: ")
            license_plate = self.extract_information(booking_email, "License Plate: ", "Vehicle Year: ")
            vehicle_year = self.extract_information(booking_email, "Vehicle Year: ", "Short")
            vehicle_description = self.extract_information(booking_email, "Vehicle Description (please include if you have a trailer): ",
                                                    "Where will you leave your keys for us to find upon pickup?: ")
            key_drop = self.extract_information(booking_email, "Where will you leave your keys for us to find upon pickup?: ", "I understand")

            # this is in case there are no special requests
            
            take_out_date = self.extract_information(booking_email, "What date are you taking out?: ", 
                                            "Any special requests, pointers, or other information for us?: ")
            special_requests = self.extract_information(booking_email, "Any special requests, pointers, or other information for us?: ", 
                                            "What amount")
            if take_out_date == None:
                take_out_date = self.extract_information(booking_email, "What date are you taking out?: ", 
                                                "What amount")
                special_requests = " "

            service_title = self.extract_information(booking_email, "Service Title: ", "With: Frank Church")
            put_in_date = self.extract_information(booking_email, "When: ", "Where: ")

            info_list = [client_name, client_email, client_phone_number, emergency_contact, emergency_contact_relation, emergency_contact_number,
            vehicle_make, vehicle_model, license_plate, vehicle_year, vehicle_description, key_drop, take_out_date,
            special_requests, service_title, put_in_date]

            self.data_dict[id] = info_list
            id = id + 1
    
    def extract_information(self, text, start_word, end_word):
        # Extracting the most important information from the email into a useable form

        start_index = text.find(start_word)
        if start_index == -1:
            print("Start keyword not found.")
            return None
        
        end_index = text.find(end_word, start_index)
        if end_index == -1:
            print("End keyword not found.")
            return None
        
        extracted_info = text[start_index + len(start_word):end_index].strip()
        extracted_info = extracted_info.rstrip("<br/>")

        return extracted_info
    
    def delete_emails_from_senders(self, sender_emails):
        # Create an instance of the API module
        gmail_api = GmailAPI()
        # Build the Gmail service
        gmail_service = gmail_api.build_gmail()

        for sender_email in sender_emails:
            # Search for emails from the specified sender
            page_token = None
            while True:
                results = gmail_service.users().messages().list(userId='me', q=f"from:{sender_email}", pageToken=page_token).execute()
                emails = results.get('messages', [])

                if not emails:
                    print(f"No emails found from {sender_email}.")
                    break

                for email in emails:
                    # Delete each email from the sender
                    gmail_service.users().messages().delete(userId='me', id=email['id']).execute()

                page_token = results.get('nextPageToken')
                if not page_token:
                    break

        print("Deleted emails from the specified senders.")

    def get_data_dict(self):
        return self.data_dict
       

