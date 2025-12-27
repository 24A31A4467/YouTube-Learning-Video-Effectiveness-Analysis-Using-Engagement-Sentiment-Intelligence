import streamlit as st
import numpy as np
import re
from googleapiclient.discovery import build
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer

# ---------------- CONFIG ----------------
st.set_page_config(page_title="YouTube Study Video Effectiveness", page_icon="📊", layout="wide")
import os

API_KEY = os.getenv("YOUTUBE_API_KEY") # Replace with your key

if not API_KEY:
    raise RuntimeError("YOUTUBE_API_KEY not found")

# ---------------- API SETUP ----------------

youtube = build("youtube", "v3", developerKey=API_KEY)

# ---------------- UTIL FUNCTIONS ----------------
def extract_video_id(url):
    match = re.search(r"(?:v=|/)([0-9A-Za-z_-]{11})", url)
    return match.group(1) if match else None

def fetch_video_metadata(video_id):
    response = youtube.videos().list(
        part="snippet,statistics",
        id=video_id
    ).execute()

    if not response["items"]:
        return None

    item = response["items"][0]
    return {
        "title": item["snippet"]["title"],
        "views": int(item["statistics"].get("viewCount", 0)),
        "likes": int(item["statistics"].get("likeCount", 0)),
        "comments": int(item["statistics"].get("commentCount", 0))
    }


def fetch_comments(video_id, max_comments=100):
    comments = []
    try:
        response = youtube.commentThreads().list(
            part="snippet",
            videoId=video_id,
            maxResults=100,
            textFormat="plainText"
        ).execute()
        for item in response.get("items", []):
            comments.append(item["snippet"]["topLevelComment"]["snippet"]["textDisplay"])
    except:
        pass
    return comments


analyzer = SentimentIntensityAnalyzer()

def compute_sentiment(comments):
    if not comments:
        return 0.0
    scores = [analyzer.polarity_scores(c)["compound"] for c in comments]
    return float(np.mean(scores))


def compute_effectiveness(metadata, avg_sentiment):
    views = metadata["views"]
    likes = metadata["likes"]
    comments = metadata["comments"]

    # Low-data penalty
    if views < 500 or (likes + comments) < 20:
        return 10.0

    engagement_density = (likes + 2 * comments) / views
    engagement_score = np.log1p(engagement_density * 100)
    sentiment_factor = 1 + np.clip(avg_sentiment, -0.2, 0.2)
    final_score = engagement_score * sentiment_factor * 25

    return final_score


def classify_video(score):
    if score >= 60:
        return "Highly Effective"
    elif score >= 30:
        return "Moderately Effective"
    else:
        return "Low Effectiveness"

# ---------------- UI ----------------
st.title("📊 YouTube Study Video Effectiveness Dashboard")
st.markdown("Analyze the **learning effectiveness** of educational YouTube videos using engagement metrics and sentiment analysis.")

url = st.text_input("Enter YouTube Video URL")

if st.button("Analyze Video"):
    if not url:
        st.warning("Please enter a YouTube URL")
    else:
        with st.spinner("Fetching and analyzing data..."):
            video_id = extract_video_id(url)
            metadata = fetch_video_metadata(video_id)
            comments = fetch_comments(video_id)
            avg_sentiment = compute_sentiment(comments)
            score = compute_effectiveness(metadata, avg_sentiment)
            label = classify_video(score)

        st.subheader("📌 Video Details")
        st.write("**Title:**", metadata["title"])

        col1, col2, col3 = st.columns(3)
        col1.metric("Views", metadata["views"])
        col2.metric("Likes", metadata["likes"])
        col3.metric("Comments", metadata["comments"])

        st.subheader("📈 Effectiveness Result")
        st.metric("Final Score", f"{score:.2f}")

        if label == "Highly Effective":
            st.success("Highly Effective Learning Video")
        elif label == "Moderately Effective":
            st.info("Moderately Effective Learning Video")
        else:
            st.error("Low Effectiveness Learning Video")

        st.subheader("🧠 Sentiment Analysis")
        st.write("Average Sentiment Score:", round(avg_sentiment, 3))

st.markdown("---")
st.caption("Rule-based analytics system using YouTube Data API & VADER sentiment analysis")
