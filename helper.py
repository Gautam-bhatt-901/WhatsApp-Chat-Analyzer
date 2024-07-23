from urlextract import URLExtract
extract = URLExtract()
from wordcloud import WordCloud
import pandas as pd
from collections import Counter
import emoji

def fetch_stats(selected_user, df):
    if selected_user != "Overall":
        df = df[df['user'] == selected_user]
    
    # 1. number of messages
    num_messages = df.shape[0]
    # 2. number of words
    words = []
    for word in df['message']:
        words.extend(word.split())

    # 3. number of media 
    num_media_messages = df[df['message'] == '<Media omitted>'].shape[0]

    # 4. number of links
    links = []
    for message in df['message']:
        links.extend(extract.find_urls(message))
    
    return num_messages, len(words), num_media_messages, len(links)

# function for most active users
def most_busy_users(df):
    x = df['user'].value_counts().head()
    df = round((df['user'].value_counts()/df.shape[0])*100,2).reset_index().rename(columns = {'user' : 'name', 'count' : 'precentage'})
    return x, df

# fuction for creating wordcloud 
def create_wordcloud(selected_user, df):
    if selected_user != "Overall":
        df = df[df['user'] == selected_user]
    
    wc = WordCloud(width = 500, height = 500, min_font_size = 10, background_color = 'white')
    df_wc = wc.generate(df['message'].str.cat(sep = " "))
    return df_wc

# function for calculating most common words
def most_common_words(selected_user, df):

    f = open('stop_hinglish.txt', 'r')
    stop_words = f.read()

    if selected_user != "Overall":
        df = df[df['user'] == selected_user]

    temp = df[df['user'] != 'group_notification']
    temp = temp[temp['message'] != "<Media omitted>"]
    
    words = []
    for message in temp['message']:
        for word in message.lower().split():
            if word not in stop_words:
                words.append(word)
    return pd.DataFrame(Counter(words).most_common(20))

# function for calculating the number of most common emojis
def emoji_helper(selected_user, df):
    
    emojis = []
    for message in df['message']:
        emojis.extend([c['emoji'] for c in emoji.emoji_list(message)])
    emoji_df = pd.DataFrame(Counter(emojis).most_common(len(emojis)))

    return emoji_df

# function for finding most bust month
def monthly_timeline(selected_user, df):
    if selected_user != "Overall":
        df = df[df['user'] == selected_user]

    timeline = df.groupby(['year', 'month']).count()['message'].reset_index()

    time = []
    for i in range(timeline.shape[0]):
        time.append(timeline['month'][i] + "-" + str(timeline['year'][i]))
    timeline['time'] = time

    return timeline

def weekly_activity_map(selected_user, df):
    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]

    return df['day_name'].value_counts()

def month_activity_map(selected_user, df):
    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]

    return df['month'].value_counts()
