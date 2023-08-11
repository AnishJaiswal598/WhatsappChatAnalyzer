import streamlit as st
import pandas as pd
import preprocessor
from io import StringIO
import helper
import matplotlib.pyplot as plt
import seaborn as sns

st.sidebar.title("Whatsapp-Chat-Analyzer")

uploaded_file = st.sidebar.file_uploader("Choose a file")
if uploaded_file is not None:
    # To read file as bytes:
    bytes_data = uploaded_file.getvalue()
    data=bytes_data.decode('utf-8')
    df=preprocessor.preprocess(data)

    unique_users=df['user'].unique().tolist()
    unique_users.remove('group_notification')
    unique_users.sort()
    unique_users.insert(0,"OverAll")
    st.title("Top Statistics: ")

    this_user=st.sidebar.selectbox("Show analysis wrt", unique_users)

    if st.sidebar.button("Show Analysis"):
        total_messages,total_words,total_media,total_urls=helper.fetch_stats(this_user,df)
        col1,col2,col3,col4=st.columns(4)
        with col1:
            st.header("Total Messages: ")
            st.title(total_messages)
        with col2:
            st.header("Total Words: ")
            st.title(total_words)
        with col3:
            st.header("Media shared: ")
            st.title(total_media)
        with col4:
            st.header("Total Urls: ")
            st.title(total_urls)

        st.title("Monthly TimeLine: ")
        df_time=helper.timeline_messages(this_user,df)
        fig,ax=plt.subplots()
        ax.plot(df_time['time'],df_time['message'],color='green')
        plt.xticks(rotation="vertical")
        st.pyplot(fig)

        st.title("Daily TimeLine: ")
        daily_time=helper.daily_timeline(this_user,df)
        fig,ax=plt.subplots()
        ax.plot(daily_time['current_date'],daily_time['message'],color='black')
        plt.xticks(rotation="vertical")
        st.pyplot(fig)

        st.title("Activity Map: ")
        col1,col2=st.columns(2)

        with col1:
            st.header("Most Busy Day: ")
            daily_time=helper.busy_days(this_user,df)
            fig,ax=plt.subplots()
            ax.bar(daily_time.index,daily_time.values,color='darkviolet')
            plt.xticks(rotation="vertical")
            st.pyplot(fig)

        with col2:
            st.header("Most Busy Month: ")
            monthly_time=helper.busy_months(this_user,df)
            fig,ax=plt.subplots()
            ax.bar(monthly_time.index,monthly_time.values,color='deeppink')
            plt.xticks(rotation="vertical")
            st.pyplot(fig)

        st.title("Weekly Activity Map")
        user_heatmap=helper.activity_heatmap(this_user,df)
        fig,ax=plt.subplots()
        ax=sns.heatmap(user_heatmap)
        st.pyplot(fig)

        if(this_user=='OverAll'):
            st.title("Most Busy Users: ")
            x,new_df=helper.get_most_active(df)
            fig,ax=plt.subplots()

            col1,col2=st.columns(2)

            with col1:
                ax.bar(x.index,x.values,color='Red')
                plt.xticks(rotation='vertical')
                st.pyplot(fig)
            with col2:
                st.dataframe(new_df)


        st.title("Word Cloud: ")
        df_wc=helper.get_worldCloud(this_user,df)
        fig,ax=plt.subplots()
        ax.imshow(df_wc)
        st.pyplot(fig)

        st.title("Most Common Words: ")
        fig,ax=plt.subplots()
        new_df=helper.get_most_common_words(this_user,df)
        ax.barh(new_df[0],new_df[1])
        plt.xticks(rotation="vertical")
        st.pyplot(fig)

        st.title("Most Common Emojis: ")
        emoji_df=helper.emoji_extractor(this_user,df)
        col1, col2 = st.columns(2)

        with col1:
            st.dataframe(emoji_df)
        with col2:
            fig, ax = plt.subplots()
            ax.pie(emoji_df[1].head(), labels=emoji_df[0].head(), autopct="%0.2f")
            st.pyplot(fig)


