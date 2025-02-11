# 🎬 TubeTalk AI – Chat with YouTube Videos!

**TubeTalk AI** is an AI-powered web app that lets you interact with YouTube videos using OpenAI's GPT-4 and Embedchain. Simply provide a YouTube video URL, and the app extracts the transcript, allowing you to ask questions and get meaningful insights instantly.

🔗 **Supports**:

✅ YouTube Videos

✅ YouTube Shorts


## 🛠 Features
* **Fetch YouTube Transcripts** – Extracts video subtitles automatically.
* **AI-Powered Q&A** – Ask any question about the video's content.
* **Memory-Powered Responses** – Uses ChromaDB to store and retrieve relevant information.
* **YouTube Shorts Support** – Works with both standard videos & shorts.
* **Fast & Easy Setup** – Just paste the video URL and start chatting!


## 🚀 How It Works

1️⃣ Enter a YouTube Video URL

2️⃣ TubeTalk AI fetches the transcript

3️⃣ Ask AI any question related to the video

4️⃣ Get instant, intelligent answers!


## 🏗 Tech Stack

* Python – The core language powering the app.
* Streamlit – A lightweight web framework for building interactive UIs.
* Embedchain – Manages both the LLM (GPT-4) and vector store (ChromaDB) for AI-powered Q&A.
* OpenAI GPT-4 – The AI model answering questions about the video.
* ChromaDB – A vector database for efficient semantic search.
* yt_dlp – Extracts video metadata, including title and thumbnails.
* YouTube Transcript API – Fetches video subtitles for processing.


## 🚀 Installation & Setup
1️⃣ Clone the Repository
    ```
    git clone https://github.com/your-username/tube-talk-ai.git
    cd tube-talk-ai
    ```
    
2️⃣ Install Dependencies
    ```
    pip install -r requirements.txt
    ```
    
3️⃣ Run the App
    ```
    streamlit run app.py
    ```


## 🔑 API Key Setup
This project requires an **OpenAI API Key** to function.

1. **Get your API key** from [here](https://platform.openai.com/signup).
2. **Enter the key** in the sidebar under "🔑 Settings" before using the app.


## 📜 License
MIT License – Free to use & modify!
