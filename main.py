# TODO 1: Make all required imports
import pandas as pd
import datetime as dt
from random import choice
import os
import smtplib
from secrets import email, password

# TODO 2: Check if today matches a birthday in the birthdays.csv
# read the csv file
birthday_data = pd.read_csv("birthdays.csv")
# list to hold all the recipients who have a birthday today
recipient_list = list()
for each_item in birthday_data.iterrows():
    temp_dict = each_item[1].to_dict()
    # if today matches a birthday => add the recipient to list
    if dt.datetime.now().month == int(temp_dict["month"]) and \
            dt.datetime.now().day == int(temp_dict["day"]):
        recipient_list.append(temp_dict)


# TODO 3: If step 2 is true, pick a random letter from letter templates
#         and replace the [NAME] with the person's actual name from birthdays.csv
def create_letter(recipient_name):
    """
    Randomly choose a letter and add recipient's name to generate final greeting
    :return: final greeting (str)
    """
    # get list of all files in letter_templates directory
    letter_dir = "letter_templates/"
    # list of letter templates
    letters = [letter for letter in os.listdir(letter_dir) if os.path.isfile(os.path.join(letter_dir, letter))]
    letter_file = choice(letters)
    with open(os.path.join(letter_dir, letter_file)) as letter_text:
        letter = letter_text.readlines()
        letter[0] = letter[0].replace("[NAME]", recipient_name)
        return ''.join(letter)


# TODO 4: Send the letter generated in step 3 to that person's email address.
for recipient in recipient_list:
    # generate email
    email_text = create_letter(recipient["name"])
    # create smtp connection
    with smtplib.SMTP("smtp.gmail.com") as connection:
        connection.starttls()
        connection.login(user=email, password=password)
        connection.sendmail(from_addr=email, to_addrs=recipient["email"], msg=f"Subject: Many Many Happy Returns of the Day\n\n{email_text}")

    print(f"Letter sent to: {recipient['name']}")



