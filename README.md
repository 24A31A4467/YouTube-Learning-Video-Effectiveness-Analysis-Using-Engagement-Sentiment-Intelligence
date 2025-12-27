# YouTube Learning Video Effectiveness Analysis Using Engagement & Sentiment Intelligence

## 📌 Project Overview
An end-to-end analytics system that evaluates the effectiveness of educational YouTube videos using real-time engagement metrics, engagement velocity (views/day, likes/day), and NLP-based sentiment analysis of comments.

## ❓ Problem Statement
Learners struggle to identify high-quality educational videos due to misleading view counts and subjective opinions. There is no objective, data-driven method to assess learning effectiveness.

## 💡 Solution
This project analyzes YouTube videos using:
- Engagement velocity (views/day, likes/day, comments/day)
- User interaction strength
- Sentiment analysis of comments using NLP

The system classifies videos as **Highly Effective**, **Moderately Effective**, or **Low Effectiveness**.

## 🚀 Key Features
- Real-time YouTube Data API integration
- Engagement normalization by video age
- NLP-based sentiment analysis (VADER)
- Interactive Streamlit dashboard
- Clear effectiveness scoring & classification

## 🛠 Tech Stack
- Python
- YouTube Data API v3
- Streamlit
- NumPy, Pandas
- NLTK (VADER Sentiment Analysis)

## ▶️ How to Run the Project
1. Clone the repository  
2. Install dependencies  
   ```bash
   pip install -r requirements.txt
3.Set your YouTube API key as an environment variable
4.Run the app
python -m streamlit run app.py
📊 Output
Displays video metadata (views, likes, comments)
Shows sentiment score
Calculates effectiveness score
Classifies learning effectiveness

⚠️ Limitations
Depends on publicly available comments
Cannot measure actual learning outcomes
API quota limits apply

🔮 Future Enhancements
ML-based effectiveness prediction
Topic-wise learning quality comparison
Viewer retention analysis
