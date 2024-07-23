import streamlit as st
import preprocessor, helper
import matplotlib.pyplot as plt

# Title
st.sidebar.title("What's App Chat Analyzer")

# make user to upload their file 
uploaded_file = st.sidebar.file_uploader("Choose a file")
if uploaded_file is not None:
    # To read file as bytes:
    bytes_data = uploaded_file.getvalue()
    data = bytes_data.decode('utf-8')
    df = preprocessor.preprocess(data)

    # fetch the name of the users in the chat 
    user_list = df['user'].unique().tolist()
    user_list.remove('group_notification')
    user_list.sort()
    user_list.insert(0, "Overall")

    selected_user = st.sidebar.selectbox("Show Analysis w.r.t", user_list)

    if st.sidebar.button("Show Analysis"):
        num_messages, words , num_media_messages, num_links= helper.fetch_stats(selected_user, df)
        
        st.title("Top Statistics")
        col1, col2, col3, col4 = st.columns(4)

        # stats area
        with col1:
            st.header("Total Messages")
            st.title(num_messages)

        with col2:
            st.header("Number of Words")
            st.title(words)
        
        with col3:
            st.header("Media Shared")
            st.title(num_media_messages)

        with col4:
            st.header("Links Shared")
            st.title(num_links)

        # Monthly activity
        st.title("Monthly Timeline")
        timeline = helper.monthly_timeline(selected_user, df)
        fig, ax = plt.subplots()
        ax.plot(timeline['time'], timeline['message'])
        plt.xticks(rotation = 'vertical')
        st.pyplot(fig)

        # Activity map
        st.title("Activity Map")
        col1, col2 = st.columns(2)

        with col1:
            st.header("Most Busy Day")
            busy_day = helper.weekly_activity_map(selected_user, df)
            fig, ax = plt.subplots()
            ax.bar(busy_day.index, busy_day.values)
            plt.xticks(rotation = 'vertical')
            st.pyplot(fig)

        with col2:
            st.header("Most Busy Month")
            busy_month = helper.month_activity_map(selected_user, df)
            fig, ax = plt.subplots()
            ax.bar(busy_month.index, busy_month.values)
            plt.xticks(rotation = 'vertical')
            st.pyplot(fig)

        # finding the busiest users in the group
        if selected_user == 'Overall':
            st.title("Most Busy Users")
            x, new_df = helper.most_busy_users(df)
            fig, ax = plt.subplots()

            col1, col2 = st.columns(2)
            with col1:
                ax.bar(x.index, x.values)
                plt.xticks(rotation = 'vertical')
                st.pyplot(fig)

            with col2:
                st.dataframe(new_df)

        # Creating WordCloud
        st.title("WordCloud")
        df_wc = helper.create_wordcloud(selected_user, df)
        fig, ax = plt.subplots()
        ax.imshow(df_wc)
        st.pyplot(fig)

        # Most Common Words
        st.title("Most Common Words")
        most_common_df = helper.most_common_words(selected_user, df)
        
        fig, ax = plt.subplots()
        ax.barh(most_common_df[0], most_common_df[1])

        st.pyplot(fig)

        # Most Common Emojis
        st.title("Most Common Emojis")
        emoji_df = helper.emoji_helper(selected_user, df)

        st.dataframe(emoji_df)







        
