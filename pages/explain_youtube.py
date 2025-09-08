#new
import streamlit as st
import google.generativeai as genai
from youtube_transcript_api import YouTubeTranscriptApi

genai.configure(api_key="Your-API-Key-Here")  

ytt_api = YouTubeTranscriptApi()

def extract_transcript_details(youtube_video_url):
    try:
        video_id = youtube_video_url.split("v=")[1].split("&")[0]
        transcript_text = ytt_api.fetch(video_id)
        transcript = " ".join(snippet.text for snippet in transcript_text)
        return transcript
    except Exception as e:
        raise e

def generate_gemini_summary(transcript_text):
    prompt = (
        "You are a YouTube video summarizer. You will be taking the transcript text "
        "and summarizing the entire video into key points and highlighting the main concepts that the user should know. "
        "Split the summary into points for every 2-3 minutes of video content for videos less than 30mins."
        "For videos extending beyoond 30mins make sure to cover all the key points and concepts in a concise manner"
        "Provide a clear, concise summary as bullet points:\n\n"
    )
    model = genai.GenerativeModel("gemini-1.5-flash")
    response = model.generate_content(prompt + transcript_text)
    return response.text

st.title("YouTube Transcript to Detailed Notes Converter")

youtube_link = st.text_input("Enter YouTube Video Link:")

if youtube_link:
    video_id = youtube_link.split("v=")[1].split("&")[0]
    st.image(f"http://img.youtube.com/vi/{video_id}/0.jpg", use_container_width=True)

    if st.button("Get Detailed Notes"):
        with st.spinner("Fetching transcript and generating summary..."):
            try:
                transcript_text = extract_transcript_details(youtube_link)
                summary = generate_gemini_summary(transcript_text)
                st.markdown("## Detailed Notes Summary:")
                # Present summary as bullet points
                for line in summary.split('\n'):
                    if line.strip():
                        st.markdown(f"- {line.strip()}")
            except Exception as e:
                st.error(f"Error obtaining transcript or summary: {e}")