import re
import pandas as pd
from datetime import datetime

def preprocess(data):
    pattern = '\d{1,2}/\d{1,2}/\d{2,4},\s\d{1,2}:\d{1,2}\s-\s'
    messages = re.split(pattern, data)[1:]
    dates = re.findall(pattern, data)
    # Define the original format
    original_format = '%m/%d/%y, %H:%M - '

    # Define the desired format
    desired_format = '%m/%d/%Y, %H:%M - '

    # List to store formatted datetime strings
    formatted_strings = []

    # Iterate through the original strings
    for original_string in dates:
        # Parse the original datetime string
        parsed_datetime = datetime.strptime(original_string, original_format)

        # Format the parsed datetime into the desired format
        formatted_datetime = parsed_datetime.strftime(desired_format)

        # Append to the list of formatted strings
        formatted_strings.append(formatted_datetime)

    df = pd.DataFrame({'message': messages, 'date': formatted_strings})
    df['date'] = pd.to_datetime(df['date'], format='%m/%d/%Y, %H:%M - ')
    users = []
    messages = []
    for message in df['message']:
        entry = re.split('([\w\W]+?):\s', message)
        if entry[1:]:  # user name
            users.append(entry[1])
            messages.append(" ".join(entry[2:]))
        else:
            users.append('group_notification')
            messages.append(entry[0])

    df['user'] = users
    df['message'] = messages

    df['year'] = df['date'].dt.year
    df['month'] = df['date'].dt.month_name()
    df['day'] = df['date'].dt.day
    df['hour'] = df['date'].dt.hour
    df['minutes'] = df['date'].dt.minute
    df['day_name'] = df['date'].dt.day_name()

    return df