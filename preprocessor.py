import re
import pandas as pd

# this function will preprocess the data and return it to app.py
def preprocess(data):
    
    # here we are finding the pattern of the date and message in order to split them form raw text
    pattern = r'\d{2}/\d{2}/\d{2}, \d{1,2}:\d{2}\u202f?[ap]m - '
    message = re.split(pattern, data)[1:]
    dates = re.findall(pattern, data)
    
    # converting the data into DataFrames 
    df = pd.DataFrame({'user_message' : message})
    df1 = pd.DataFrame({'date' : dates})
    df = pd.concat([df, df1], axis = 1, join = 'inner')
    df.user_message = df.user_message.str.strip()
    df.date = pd.to_datetime(df['date'], format = '%d/%m/%y, %I:%M %p - ', errors='coerce')

    # here we are further splitting the user(the one who sent the message) and message and creating different columns for easy processing
    user = []
    message = []
    for msg in df.user_message:
        entry = re.split('([\w\W]+?):\s', msg)
        if entry[1:]:
            user.append(entry[1])
            message.append(entry[2])
        else:
            user.append("group_notification")
            message.append(entry[0])
    df['user'] = user
    df['message'] = message
    df.drop(columns = ['user_message'], inplace = True)

    # here we are splitting the date column into more specific column(year, month, day, time) and creating their own column
    df['year'] = df['date'].dt.year
    df['month'] = df['date'].dt.month_name()
    df['day'] = df['date'].dt.day
    df['day_name'] = df['date'].dt.day_name()
    df['time'] = df['date'].dt.strftime('%I:%M %p')

    return df