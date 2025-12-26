import streamlit as st
import preprocessor,helper
import matplotlib.pyplot as plt
import plotly_express as px

st.markdown(
    """
    <style>
    /* Make metric labels same height */
    div[data-testid="stMetricLabel"] {
        min-height: 48px;
        display: flex;
        align-items: center;
        justify-content: center;
        text-align: center;
        font-size: 18px;
    }

    /* Metric value styling */
    div[data-testid="stMetricValue"] {
        font-size: 40px;
        font-weight: 700;
    }
    </style>
    """,
    unsafe_allow_html=True
)


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

    #Analysis Type
    analysis_type=st.sidebar.selectbox("📊 Select Analysis",
                                       ["Top Statistics",
                                        "Timeline",
                                        "Activity Map",
                                        "Word Cloud",
                                        "Emoji Analysis"]
                                       )

    # --- [START] NEW CODE: WORD CLOUD SHAPE SELECTION ---
    # We initialize mask_image to None by default
    mask_image = None

    # Only show these options if the user selected "Word Cloud"
    if analysis_type == "Word Cloud":
        st.sidebar.markdown("---")
        st.sidebar.header("☁️ Word Cloud Shape")

        shape_mode = st.sidebar.radio(
            "Select Shape Source:",
            ("Default (Rectangle)", "Upload Custom Image", "Choose Preset")
        )

        if shape_mode == "Upload Custom Image":
            uploaded_mask = st.sidebar.file_uploader("Upload Transparent PNG", type=['png'])
            if uploaded_mask is not None:
                mask_image = uploaded_mask

        elif shape_mode == "Choose Preset":
            # NOTE: You must have these files in your project folder!
            preset_choice = st.sidebar.selectbox("Select Shape:", ["Twitter Logo", "Heart", "Chat Bubble"])

            if preset_choice == "Twitter Logo":
                mask_image = "masks/images.png"  # Replace with your actual file name
            elif preset_choice == "Heart":
                mask_image = "masks/download (1).png"  # Replace with your actual file name
            elif preset_choice == "Chat Bubble":
                mask_image = "masks/download.png"  # Replace with your actual file name
    # --- [END] NEW CODE ---

    show_analysis = st.sidebar.button("🚀 Show Analysis")
    if show_analysis:
        if analysis_type=="Top Statistics":
            #Stats Area
            st.title("📈 Top Statistics")
            num_messages,words,num_media_messages,num_links=helper.fetch_stats(selected_user,df)
            col1,col2,col3,col4=st.columns(4)

            with col1:
                st.metric("💬 Total Messages", num_messages)
            with col2:
                st.metric("📝 Total Words", words)
            with col3:
                st.metric("🖼️ Media Shared/Received", num_media_messages)
            with col4:
                st.metric("🔗 Links Shared/Received", num_links)


            # Finding the busiest users in the groups(Group Level)
            if selected_user == 'Overall':
                st.title("🚀 MOST BUSY USERS")
                x, new_df = helper.most_busy_users(df)
                fig, ax = plt.subplots()

                col1, col2 = st.columns(2)

                with col1:
                    ax.bar(x.index, x.values, color='green')
                    plt.xticks(rotation='vertical')
                    st.pyplot(fig)
                with col2:
                    st.dataframe(new_df)
        if analysis_type=="Timeline":
            # Daily_Timeline
            st.title("⏰📅 Daily Message Trend")
            daily_timeline = helper.daily_timeline(selected_user, df)
            fig, ax = plt.subplots()
            ax.plot(daily_timeline['date_timeline'], daily_timeline['message'], color='violet')
            plt.xticks(rotation='vertical')
            plt.grid()

            st.pyplot(fig)


            #Monthly_Timeline
            st.title("📅 Monthly Message Trend")
            timeline=helper.monthly_timeline(selected_user,df)
            fig,ax=plt.subplots()
            ax.plot(timeline['time'], timeline['message'],color='red')
            plt.xticks(rotation='vertical')
            plt.grid()

            st.pyplot(fig)

        if analysis_type=="Activity Map":
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

        if analysis_type=="Word Cloud":
            #Word Cloud
            st.title("☁️ WordCloud")
            df_wc=helper.create_wordcloud(selected_user, df,mask_image=mask_image)
            fig,ax=plt.subplots()
            ax.imshow(df_wc)
            ax.axis("off")
            st.pyplot(fig)

            #Most common words used in chats
            st.title("📌 Most Common Words Used")
            most_common_df=helper.most_common_words(selected_user,df)

            fig,ax=plt.subplots()
            ax.barh(most_common_df[0],most_common_df[1])
            st.pyplot(fig)

        if analysis_type=="Emoji Analysis":
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
