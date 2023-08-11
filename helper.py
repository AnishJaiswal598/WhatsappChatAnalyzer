from urlextract import URLExtract
extractor=URLExtract()
from wordcloud import WordCloud
from collections import Counter
import pandas as pd
import emoji

def fetch_stats(selected_user,df):
    total_messages=0
    words=[]
    media_files=0
    links=[]
    if (selected_user != 'OverAll'):
        new_df = df[df['user'] == selected_user]
        df=new_df

    total_messages =df.shape[0]
    for mess in df['message']:
        links.extend(extractor.find_urls(mess))
        words.extend(mess.split(' '))
    df2=df[df['message']=='<Media omitted>\n']
    media_files=df2.shape[0]

    return total_messages,len(words),media_files,len(links)

def get_most_active(df):
    df = df[df['user'] != 'group_notification']
    x = df['user'].value_counts().head()
    df = round((df['user'].value_counts() / df.shape[0]) * 100, 2).reset_index().rename(
        columns={'index': 'name', 'user': 'percent'})
    return  x,df

def get_worldCloud(selected_user,df):
    if(selected_user!='OverAll'):
        df=df[df['user']==selected_user]

    new_df = df[df['user'] != 'group_notification']
    new_df = new_df[new_df['message'] != '<Media omitted>\n']

    f = open('stopWord.txt', 'r')
    stop_words = f.read()
    def remove_stop_word(message):
        words=[]
        for word in message.lower().split():
            if word not in stop_words :
                words.append(word)
        return " ".join(words)

    new_df['message']=new_df['message'].apply(remove_stop_word)
    wc=WordCloud(width=500,height=500,min_font_size=10,background_color='white')
    df_wc=wc.generate(new_df['message'].str.cat(sep=" "))
    return df_wc


# most common words
def get_most_common_words(selected_user,df):
    if(selected_user!='OverAll'):
        df = df[df['user'] == selected_user]

    new_df = df[df['user'] != 'group_notification']
    new_df = new_df[new_df['message'] != '<Media omitted>\n']

    f = open('stopWord.txt', 'r')
    stop_words = f.read()

    words = []
    for message in new_df['message']:
        for word in message.lower().split():
            if word not in stop_words:
                words.append(word)

    return pd.DataFrame(Counter(words).most_common(20))

def emoji_extractor(selected_user,df):
    if(selected_user!='OverAll'):
        df = df[df['user'] == selected_user]

    words = []
    for messages in df['message']:
        words.extend(messages.split())

    mystr = ""
    for x in words:
        mystr = mystr + " " + x

    myemoji = emoji.emoji_list(mystr)

    pre_final_emoji_list = []
    for i in range(len(myemoji)):
        pre_final_emoji_list.extend(myemoji[i]['emoji'])

    emojis_to_be_removed = ['', '🏻']

    final_emoji_list = []
    for items in pre_final_emoji_list:
        if items not in emojis_to_be_removed:
            final_emoji_list.append(items)

    emoji_df=pd.DataFrame(Counter(final_emoji_list).most_common(len(final_emoji_list)))
    return emoji_df

def timeline_messages(selected_user,df):
    if(selected_user!='OverAll'):
        df = df[df['user'] == selected_user]
    df['month_num'] = df['date'].dt.month
    timeline = df.groupby(['year', 'month_num', 'month']).count()['message'].reset_index()
    time = []
    for i in range(timeline.shape[0]):
        time.append(timeline['month'][i] + "-" + str(timeline['year'][i]))
    timeline['time'] = time
    return timeline

def daily_timeline(selected_user,df):
    if(selected_user!='OverAll'):
        df = df[df['user'] == selected_user]
    df['current_date'] = df['date'].dt.date
    daily_timeline = df.groupby('current_date').count()['message'].reset_index()
    return daily_timeline

def busy_days(selected_user,df):
    if(selected_user!='OverAll'):
        df = df[df['user'] == selected_user]
    df['day_name']=df['date'].dt.day_name()
    return df['day_name'].value_counts()

def busy_months(selected_user,df):
    if(selected_user!='OverAll'):
        df = df[df['user'] == selected_user]
    return df['month'].value_counts()

def activity_heatmap(selected_user,df):
    if(selected_user!='OverAll'):
        df = df[df['user'] == selected_user]
    period = []
    for hour in df[['day_name', 'hour']]['hour']:
        if hour == 23:
            period.append(str(hour) + "-" + "00")
        elif hour == 0:
            period.append(str(hour) + "-" + "01")
        else:
            period.append(str(hour) + "-" + str(hour + 1))

    df['period'] = period
    user_heatmap = df.pivot_table(index='day_name', columns='period', values='message', aggfunc='count').fillna(0)
    return user_heatmap



