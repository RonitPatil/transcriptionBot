import streamlit as st
from lyzr import VoiceBot, Summarizer
from saveAudio import download_instagram_reel, download_youtube_video


vb = VoiceBot(api_key=st.secrets["OPENAI_API_KEY"])

def process_url(url, download_path):
    if "instagram.com" in url:
        return download_instagram_reel(url, download_path)
    elif "youtube.com" in url or "youtu.be" in url:
        return download_youtube_video(url, download_path)
    else:
        st.markdown("### Please provide a valid URL from Instagram or YouTube.")

with st.sidebar:
    st.markdown("### Enter URL before asking a question")
    url = st.text_area("Enter URL:", key="url_uploader", label_visibility='hidden')

if url:
    file_path, caption, duration = process_url(url, "data")

    if file_path:
        transcript = vb.transcribe(file_path)
        summarizer = Summarizer(api_key=st.secrets["OPENAI_API_KEY"])
        text=transcript
        summary = summarizer.summarize(text)
        st.markdown("### Caption")
        st.write(caption)
        st.markdown("### Transcript")
        st.write(transcript)
        if duration>=60: 
            st.markdown("### Summary")
            st.write(summary)
    else:
        st.error("Failed to download or process the video.")
