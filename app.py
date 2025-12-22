import streamlit as st
import preprocessor,helper
import matplotlib.pyplot as plt
import plotly_express as px
st.sidebar.title("🟢✆ WhatsApp Chat Analyzer")
st.sidebar.markdown("📊 Analyze your WhatsApp conversations visually")

st.sidebar.header("⚙️ Controls")

uploaded_file = st.sidebar.file_uploader(
    "📂 Upload WhatsApp Chat File",
    type=["txt"]
)
if uploaded_file is not None:
    # To read file as bytes:
    bytes_data = uploaded_file.getvalue()
    # To convert it into string
    data=bytes_data.decode("utf-8")
    #st.text(data) //This is optional or no need, shows data in the form of string which we decode
    df=preprocessor.preprocess(data)


    #fetch unique users
    user_list=df['user'].unique().tolist()
    user_list.remove("group_notification")
    user_list.sort()
    user_list.insert(0,"Overall")

    selected_user = st.sidebar.selectbox(
        "👤 Show analysis for",
        user_list
    )

    show_analysis = st.sidebar.button("📊 Show Analysis")
    if show_analysis:
        #Stats Area
        st.title("📈 Top Statistics")
        num_messages,words,num_media_messages,num_links=helper.fetch_stats(selected_user,df)
        col1,col2,col3,col4=st.columns(4)

        with col1:
            st.header("💬 Total Messages")
            st.title(num_messages)
        with col2:
            st.header("📝 Total Words")
            st.title(words)
        with col3:
            st.header("🖼️ Media Shared/Received")
            st.title(num_media_messages)
        with col4:
            st.header("🔗 Links Shared/Received")
            st.title(num_links)

        # Daily_Timeline
        st.title("📅 Daily Timeline of WhatsApp Chats")
        daily_timeline = helper.daily_timeline(selected_user, df)
        fig, ax = plt.subplots()
        ax.plot(daily_timeline['date_timeline'], daily_timeline['message'], color='violet')
        plt.xticks(rotation='vertical')
        plt.grid()

        st.pyplot(fig)


        #Monthly_Timeline
        st.title("📅 Monthly Timeline of WhatsApp Chats")
        timeline=helper.monthly_timeline(selected_user,df)
        fig,ax=plt.subplots()
        ax.plot(timeline['time'], timeline['message'],color='red')
        plt.xticks(rotation='vertical')
        plt.grid()

        st.pyplot(fig)

        #Activity Map
        st.title("🗺️ Activity Map")
        col1,col2=st.columns(2)

        with col1:
            st.header("📅 Most Busy Day")
            busy_day=helper.weekly_activity_map(selected_user, df)
            fig,ax=plt.subplots()
            ax.bar(busy_day.index,busy_day.values)
            plt.xticks(rotation='vertical')
            st.pyplot(fig)

        with col2:
            st.header("📈 Most Busy Month")
            busy_month=helper.monthly_activity_map(selected_user, df)
            fig,ax=plt.subplots()
            ax.bar(busy_month.index,busy_month.values,color='#00008B')
            plt.xticks(rotation='vertical')
            st.pyplot(fig)

        #Weekly Activity Heatmap using plotly

        st.title("⏰📊 Weekly Activity Heatmap")
        user_activity_heatmap=helper.activity_heatmap(selected_user, df)
        fig = px.imshow(
            user_activity_heatmap,
            color_continuous_scale='turbo',
            labels=dict(x="Time Period", y="Day", color="Messages"),
            aspect="auto"
        )

        # IMPORTANT: Force categorical axis
        fig.update_xaxes(type='category')
        fig.update_yaxes(type='category')

        fig.update_layout(width=1200, height=450)

        st.plotly_chart(fig, use_container_width=True)


        # Finding the busiest users in the groups(Group Level)
        if selected_user=='Overall':
            st.title("🚀 MOST BUSY USERS")
            x,new_df=helper.most_busy_users(df)
            fig,ax=plt.subplots()


            col1 ,col2=st.columns(2)

            with col1:
                ax.bar(x.index, x.values,color='green')
                plt.xticks(rotation='vertical')
                st.pyplot(fig)
            with col2:
                st.dataframe(new_df)

        #Word Cloud
        st.title("☁️ WordCloud")
        df_wc=helper.create_wordcloud(selected_user, df)
        fig,ax=plt.subplots()
        ax.imshow(df_wc)
        st.pyplot(fig)

        #Most common words used in chats
        st.title("📌 Most Common Words Used")
        most_common_df=helper.most_common_words(selected_user,df)

        fig,ax=plt.subplots()
        ax.barh(most_common_df[0],most_common_df[1])
        st.pyplot(fig)

        # emoji analysis
        emoji_df = helper.emoji_helper(selected_user, df)
        st.title("😄 Emoji Analysis")
        col1, col2 = st.columns(2)

        with col1:
            st.dataframe(emoji_df)
        with col2:
            fig = px.treemap(
                emoji_df,
                path=[0],
                values=1,
                labels={0: 'Emoji', 1: 'Count'},
                color=1,
                color_continuous_scale='viridis'
            )
            st.plotly_chart(fig, use_container_width=True)


        left, center, right = st.columns([1, 2, 1])  # center column is wider
        with center:
            top_5 = emoji_df.head(5)
            fig, ax = plt.subplots(figsize=(5, 5))
            ax.pie(
                top_5[1],
                labels=top_5[0],
                autopct="%1.1f%%",
                startangle=140
            )
            st.pyplot(fig)

st.sidebar.markdown("---")
st.sidebar.markdown("🚀 Built with Streamlit")
st.sidebar.markdown("💚 Made for WhatsApp Data Analysis")
