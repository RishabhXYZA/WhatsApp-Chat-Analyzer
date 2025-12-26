📱 WhatsApp Chat Analyzer
WhatsApp Chat Analyzer is a Python and Streamlit-based tool for exploring WhatsApp chat exports. It parses raw text files and turns them into interactive statistics and visualizations. Understand participation, activity patterns, content trends, and emoji usage in just a few clicks! 🚀

📖 Introduction
This project helps you turn your WhatsApp conversations into structured insights. After exporting a chat, the app parses each message to aggregate metrics with a focus on clarity and interactivity. Perfect for both group chats and individual conversations! 📊

Code snippet

flowchart TD
    A[📩 Export chat text file] --> B[📤 Upload in Streamlit app]
    B --> C[⚙️ Parse dates, users, and content]
    C --> D[📈 Compute statistics and trends]
    D --> E[🖼️ Show charts, tables, and word clouds]
✨ Features
📊 Overall Summary: Total messages, words, media, and links.

🏆 Top Participants: See who the most active users are.

📅 Activity Timelines: Track daily, weekly, and monthly trends.

🔥 Heatmaps: Identify peak activity by weekday and hour.

☁️ Word Clouds: Visualize common words (customizable!).

😂 Emoji Analysis: Discover the most used emojis and their distribution.

🔗 Content Detection: Easy identification of shared links and media.

🌐 Web Interface: A clean Streamlit UI that runs in your browser.

[!IMPORTANT] Output is local only. All analysis runs locally on your machine for maximum privacy! 🔒

🛠️ Requirements
Python: 3.8+ 🐍

Browser: Chrome, Edge, or Firefox 🌐

Libraries: streamlit, pandas, matplotlib, seaborn, wordcloud, emoji, urlextract.

⚙️ Installation & Usage
Clone the repo: git clone https://github.com/RishabhXYZA/WhatsApp-Chat-Analyzer.git

Install: pip install -r requirements.txt

Run: streamlit run app.py 🚀

🤝 Contributing
Contributions are welcome! Please fork the repository and open a Pull Request. ✨

⚖️ License
This project is licensed under the MIT License. See the LICENSE file for the full legal text. 📝
