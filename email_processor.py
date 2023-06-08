# email_processor.py
import re

class EmailProcessor:
    def __init__(self):
        pass

    def extract_details(self, email):
        # Implement the logic to extract relevant details from the email
        # You can use regular expressions, string parsing, or any other method
        # Return a dictionary or object containing the extracted details

        subject = self.extract_subject(email)
        body = self.extract_body(email)

        details = {
            'subject': subject,
            'body': body
        }

        return details

    def extract_subject(self, email):
        # Implement the logic to extract the subject from the email
        # Return the extracted subject

        return email.subject

    def extract_body(self, email):
        # Implement the logic to extract the body content from the email
        # Return the extracted body content

        return email.body

    # Implement other methods for email processing, if required
