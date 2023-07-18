import base64
import json
import os
import subprocess
import tkinter as tk
from email_processor import EmailProcessor
from event_creator import EventCreator

'''
def delete_emails():
    # Get the emails to delete from the input field
    emails_to_delete = emails_input.get()
    
    # Create an instance of the EmailProcessor
    email_processor = EmailProcessor()
    email_processor.delete_emails_from_senders(emails_to_delete)'''

def start_process():

    # Open the txt file in write mode and delete contents
    with open("bookings_that_need_manual_addition.txt", "w") as file:
        file.truncate(0)

    # Create an instance of the EmailProcessor
    email_processor = EmailProcessor()

    # Perform the email processing and event creation logic
    booking_emails = email_processor.start_process()
    data = email_processor.set_data_dict(booking_emails)
    data_dict = email_processor.get_data_dict()

    #Create a new calendar event for each booking with details from the email
    for i in data_dict:
        event_data = data_dict[i]
        event_creator = EventCreator()
        calendar_service = event_creator.start_process()
        event_creator.create_booking_event(calendar_service, event_data)

    filepth = "C:/Users/daisy/Documents/GitHub/ShuttlePlan/bookings_that_need_manual_addition.txt"
    # Open the text document using the default associated application
    subprocess.call(["start", filepth], shell=True)

def calculate_schedule():

    time_min = '2023-06-01T00:00:00Z'
    event_creator = EventCreator()
    calendar_service = event_creator.start_process()

    overlapping_groups = event_creator.get_events(calendar_service, time_min)
    main_dates, middle_dates = event_creator.calc_drives(overlapping_groups)  
    event_creator.make_drive_events(calendar_service, main_dates, middle_dates) 
    

# Create the Tkinter window
window = tk.Tk()
window.title("FCRS Schedule Planner")
window.geometry("400x200")

'''
# Add a label and input field for emails to delete
emails_label = tk.Label(window, text="Sender email address of emails to delete: ")
emails_label.pack()

emails_input = tk.Entry(window)
emails_input.pack()

# Add a button to delete emails
delete_emails_button = tk.Button(window, text="Delete Emails", command=delete_emails)
delete_emails_button.pack()
'''


# Add a label for the instructions
instructions_label = tk.Label(window, text="Welcome to the FCRS Schedule Planner Tool. \n You can add bookings to the calendar, calculate the schedule, or both.")
#instructions_label.pack(anchor=tk.NW, padx=10, pady=10)


# Add a button to start the process
start_button = tk.Button(window, text="Add Bookings to Calendar", command=start_process)
start_button.config(bg="#BFE0EE")  
#start_button.pack()

# Add a label for the instructions
instructions_label2 = tk.Label(window, text="Press calculate to calculate the most efficient schedule,\n    make sure you have added all the events that need manual addition first")
#instructions_label.pack(anchor=tk.NW, padx=10, pady=10)

# Add a button to calculate the schedule
calculate_schedule_button = tk.Button(window, text="Calculate Schedule", command=calculate_schedule)
calculate_schedule_button.config(bg="#BFE0EE")  
#calculate_schedule_button.pack()

spacer1 = tk.Label(window, text="", height=1)
spacer2 = tk.Label(window, text="", height=1)
spacer3 = tk.Label(window, text="", height=1)

instructions_label.grid(row=0, column=0)
spacer1.grid(row=1, column=0)

start_button.grid(row=2, column=0)
spacer2.grid(row=3, column=0)

instructions_label2.grid(row=4, column=0)
spacer3.grid(row=5, column=0)

calculate_schedule_button.grid(row=6, column=0)

# Start the Tkinter event loop
window.mainloop()
