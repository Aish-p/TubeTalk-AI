import tempfile
import streamlit as st
from embedchain import App
from youtube_transcript_api import YouTubeTranscriptApi
import yt_dlp
from typing import Tuple

# Function to initialize Embedchain bot
def embedchain_bot(db_path: str, api_key: str) -> App:
    return App.from_config(
        config={
            "llm": {"provider": "openai", "config": {"model": "gpt-4", "temperature": 0.5, "api_key": api_key}},
            "vectordb": {"provider": "chroma", "config": {"dir": db_path}},
            "embedder": {"provider": "openai", "config": {"api_key": api_key}},
        }
    )

# Extract video ID from URL
def extract_video_id(video_url: str) -> str:
    if "youtube.com/watch?v=" in video_url:
        return video_url.split("v=")[-1].split("&")[0]
    elif "youtube.com/shorts/" in video_url:
        return video_url.split("/shorts/")[-1].split("?")[0]
    else:
        raise ValueError("Invalid YouTube URL")

# Fetch video title & transcript
def fetch_video_data(video_url: str) -> Tuple[str, str, str]:
    try:
        video_id = extract_video_id(video_url)

        # Fetch video metadata using yt_dlp
        ydl_opts = {"quiet": True}
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info_dict = ydl.extract_info(video_url, download=False)
            video_title = info_dict.get("title", "Unknown Title")
            thumbnail_url = info_dict.get("thumbnail", "")

        # Fetch transcript
        transcript = YouTubeTranscriptApi.get_transcript(video_id)
        transcript_text = " ".join([entry["text"] for entry in transcript])

        return video_title, transcript_text, thumbnail_url
    except Exception as e:
        st.error(f"Error fetching video data: {e}")
        return "Unknown Title", "No transcript available for this video.", ""

# Streamlit UI starts here
st.set_page_config(page_title="Chat with YouTube Videos - YouTube Video Chat", page_icon="📺", layout="wide")

# Sidebar for API Key & About Section
st.sidebar.title("🔑 Settings")
st.sidebar.markdown("### Enter Your OpenAI API Key:")
openai_access_token = st.sidebar.text_input(
    "🔑 API Key", 
    type="password", 
    help="Your OpenAI API Key is required to generate responses."
)

# Custom styling for API Key input
st.sidebar.markdown(
    """
    <style>
    div[data-baseweb="input"] {
        font-size: 18px !important;
        padding: 10px !important;
    }
    </style>
    """, 
    unsafe_allow_html=True
)

st.sidebar.markdown("---")

# About Section in Sidebar
st.sidebar.markdown("## ℹ️ About This App")
st.sidebar.markdown(
    """
    **TubeTalk AI** is an AI-powered tool that lets you ask questions about a YouTube video's content. 
    Simply provide a video URL, and the app will extract the transcript so you can chat with it.
    
    - 🎥 **Fetch Video & Shorts Transcripts**
    - 💬 **Ask AI Questions About Video Content**
    - 🤖 **Powered by OpenAI & Embedchain**
    - 🔗 **Supports YouTube Videos & Shorts**
    """
)

st.sidebar.markdown("---")

st.title("🎬 TubeTalk AI")
st.markdown("💬 **Ask questions about a YouTube video using AI-powered chat!**")

if openai_access_token:
    db_path = tempfile.mkdtemp()
    app = embedchain_bot(db_path, openai_access_token)

    # YouTube Video URL input
    video_url = st.text_input("📺 Enter YouTube Video URL", placeholder="https://www.youtube.com/watch?v=xxxxxxx")
    
    if video_url:
        try:
            title, transcript, thumbnail_url = fetch_video_data(video_url)
            
            # Display video details
            with st.container():
                col1, col2 = st.columns([1, 3])
                if thumbnail_url:
                    col1.image(thumbnail_url, use_container_width=True)
                col2.markdown(f"### 🎥 {title}")
                col2.markdown(f"[🔗 Watch on YouTube]({video_url})")
            
            st.divider()
            
            if transcript != "No transcript available for this video.":
                app.add(transcript, data_type="text", metadata={"title": title, "url": video_url})
                st.success(f"✅ **'{title}' has been added to the knowledge base!**")
            else:
                st.warning(f"⚠️ No transcript available for **'{title}'**. Cannot add to knowledge base.")

        except Exception as e:
            st.error(f"🚨 Error: {e}")

        # User input for chatbot
        with st.form("chat_form"):
            prompt = st.text_input("💡 Ask anything about the video", placeholder="e.g., What is the main topic of this video?")
            submit_button = st.form_submit_button("Ask AI")

        if submit_button and prompt:
            try:
                with st.spinner("Thinking... 🤔"):
                    answer = app.chat(prompt)
                st.success("💡 AI Response:")
                st.write(answer)
            except Exception as e:
                st.error(f"🚨 Error: {e}")

else:
    st.warning("⚠️ Please enter your OpenAI API Key in the sidebar to continue.")
