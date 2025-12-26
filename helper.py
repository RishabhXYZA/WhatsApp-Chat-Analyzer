from urlextract import URLExtract
from wordcloud import WordCloud
import pandas as pd
from collections import Counter
import emoji
import numpy as np
from PIL import Image

extract=URLExtract()
def fetch_stats(selected_user,df):
    if selected_user!='Overall':
        df=df[df['user']==selected_user]
    #Fetch number of messages
    num_messages=df.shape[0]

    #Fetch total number of words
    words=[]
    for message in df['message']:
        words.extend(message.split())

    #Fetch number of media messages
    num_media_messages=df[df['message']=='<Media omitted>\n'].shape[0]

    #Fetch number of links shared
    links=[]
    for message in df['message']:
        links.extend(extract.find_urls(message))

    return num_messages,len(words),num_media_messages,len(links)

def most_busy_users(df):
    x = df['user'].value_counts().head()
    df=(round((df['user'].value_counts()/df.shape[0])*100,2).reset_index().
        rename(columns={'user':'Name','count':'Percent'}))
    return x,df

def create_wordcloud(selected_user,df,mask_image=None):
    f = open('stop_hinglish.txt', 'r')
    stopwords = f.read()

    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]


    temp = df[df['user'] != 'group_notification']
    temp = temp[temp['message'] != '<Media omitted>\n']


    def remove_stop_words(message):
        y=[]
        for word in message.lower().split():
            if word not in stopwords:
                y.append(word)
        return " ".join(y)
    temp['message'] = temp['message'].apply(remove_stop_words)

    #Configure a WordCloud object using Wordcloud Class
    wc_params={"width":1000,
               "height":1000,
               "min_font_size":10,
               "background_color":'white'}
    if mask_image is not None:
        # Load the image and force RGBA (fixes "Bad transparency mask" error)
        icon=Image.open(mask_image).convert("RGBA")
        new_size = (1000, 1000)
        icon = icon.resize(new_size, Image.Resampling.LANCZOS)
        # Create a white background to replace transparency
        white_bg = Image.new("RGB", icon.size, (255, 255, 255))
        white_bg.paste(icon, (0, 0), icon)

        # Convert to numpy array for WordCloud
        mask_array = np.array(white_bg)

        # Add mask-specific parameters
        wc_params["mask"] = mask_array
        wc_params["contour_width"] = 3
        wc_params["contour_color"] = 'black'
        wc_params["max_words"]=60
    wc=WordCloud(**wc_params)
    df_wc= wc.generate(temp['message'].str.cat(sep=" "))
    return df_wc

def most_common_words(selected_user,df):
    f=open('stop_hinglish.txt','r')
    stopwords=f.read()

    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]
    temp = df[df['user'] != 'group_notification']
    temp = temp[temp['message'] != '<Media omitted>\n']

    words = []

    for message in temp['message']:
        for word in message.lower().split():
            if word not in stopwords:
                words.append(word)
    most_common_df=pd.DataFrame(Counter(words).most_common(20))
    return most_common_df

def emoji_helper(selected_user,df):
    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]

    emojis = []
    for message in df['message']:
        for c in message:
            if emoji.is_emoji(c):
                emojis.append(c)

    emoji_df=pd.DataFrame(Counter(emojis).most_common(len(Counter(emojis))))

    return emoji_df

def monthly_timeline(selected_user,df):
    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]

    timeline = df.groupby(['year', 'month_num', 'month']).count()['message'].reset_index()

    time = []
    for i in range(timeline.shape[0]):
        time.append(timeline['month'][i] + "-" + str(timeline['year'][i]))

    timeline['time'] = time

    return timeline

def daily_timeline(selected_user,df):
    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]

    daily_timeline = df.groupby('date_timeline').count()['message'].reset_index()
    return daily_timeline


def weekly_activity_map(selected_user, df):
    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]

    return df['day_name'].value_counts()

def monthly_activity_map(selected_user,df):
    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]

    return df['month'].value_counts()

def activity_heatmap(selected_user,df):
    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]
    user_activity_heatmap=df.pivot_table(
        index='day_name',
        columns='period',
        values='message',
        aggfunc='count'
    ).fillna(0)

    return user_activity_heatmap

