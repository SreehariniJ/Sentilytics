import streamlit as st
import pandas as pd
from textblob import TextBlob
import plotly.express as px
from wordcloud import WordCloud
import matplotlib.pyplot as plt

# 🌐 Page config
st.set_page_config(page_title="Sentilytics", page_icon="💬", layout="centered")

# 💡 Custom CSS for styling
st.markdown("""
    <style>
        body {
            background-color: #f9f9f9;
        }
        .main-title {
            text-align: center;
            font-size: 42px;
            color: #6C63FF;
            margin-bottom: 5px;
        }
        .subtitle {
            text-align: center;
            font-size: 20px;
            color: #444;
            margin-top: 0;
            margin-bottom: 20px;
        }
        .section-title {
            margin-top: 30px;
            font-size: 20px;
            font-weight: 600;
            color: #333;
        }
        .stTextArea textarea {
            background-color: #ffffff !important;
            font-size: 16px !important;
        }
    </style>
""", unsafe_allow_html=True)

# 🏷️ Title section
st.markdown("<div class='main-title'>💬 Sentilytics</div>", unsafe_allow_html=True)
st.markdown("<div class='subtitle'>Emotion Tracking for the Digital Age</div>", unsafe_allow_html=True)
st.markdown("<hr style='border: 1px solid #ddd;'>", unsafe_allow_html=True)

# 📌 Sidebar navigation
st.sidebar.title("🔍 Sentilytics")
mode = st.sidebar.radio("Choose Analysis Mode", ["📝 Analyze Single Text", "📂 Analyze CSV File"])

# 🧠 Helper Functions
def analyze_sentiment(text):
    polarity = TextBlob(str(text)).sentiment.polarity
    if polarity > 0.1:
        return "Positive"
    elif polarity < -0.1:
        return "Negative"
    return "Neutral"

def generate_wordcloud(texts):
    wc = WordCloud(width=800, height=300, background_color='white').generate(' '.join(texts))
    fig, ax = plt.subplots(figsize=(10, 4))
    ax.imshow(wc, interpolation='bilinear')
    ax.axis("off")
    st.pyplot(fig)

def plot_distribution(df):
    fig = px.bar(
        df['Sentiment'].value_counts().reset_index(),
        x='index', y='Sentiment',
        labels={'index': 'Sentiment', 'Sentiment': 'Count'},
        color='index',
        color_discrete_map={
            'Positive': '#2ecc71',
            'Negative': '#e74c3c',
            'Neutral': '#95a5a6'
        },
        title='📊 Sentiment Distribution'
    )
    fig.update_layout(showlegend=False)
    st.plotly_chart(fig, use_container_width=True)

# 📝 Mode 1: Analyze Single Text
if mode == "📝 Analyze Single Text":
    st.markdown("<div class='section-title'>📝 Enter Your Text</div>", unsafe_allow_html=True)
    user_input = st.text_area("", placeholder="Write a review, opinion, or feedback...")

    if st.button("Analyze Text"):
        if user_input.strip():
            result = analyze_sentiment(user_input)
            polarity = TextBlob(user_input).sentiment.polarity
            emoji = "🟢" if result == "Positive" else "🔴" if result == "Negative" else "🟡"
            st.success(f"**Sentiment:** {result} {emoji} &nbsp; | &nbsp; **Polarity Score:** `{polarity:.2f}`")
            st.progress(abs(polarity))
        else:
            st.warning("⚠️ Please enter valid text.")

# 📂 Mode 2: Analyze CSV
elif mode == "📂 Analyze CSV File":
    st.markdown("<div class='section-title'>📂 Upload CSV File</div>", unsafe_allow_html=True)
    uploaded_file = st.file_uploader("Upload your CSV file (must contain a text column)", type=["csv"])

    if uploaded_file:
        df = pd.read_csv(uploaded_file)
        st.success("✅ File uploaded successfully")
        st.dataframe(df.head())

        text_col = st.selectbox("Select the text column for sentiment analysis:", df.columns)

        if st.button("Run Sentiment Analysis"):
            df["Sentiment"] = df[text_col].apply(analyze_sentiment)
            st.success("✅ Sentiment analysis complete!")
            st.dataframe(df.head())

            st.markdown("<div class='section-title'>📊 Sentiment Distribution</div>", unsafe_allow_html=True)
            plot_distribution(df)

            st.markdown("<div class='section-title'>☁️ Word Cloud</div>", unsafe_allow_html=True)
            generate_wordcloud(df[text_col].astype(str))

            csv = df.to_csv(index=False).encode("utf-8")
            st.download_button("⬇️ Download CSV with Sentiment", csv, "sentilytics_output.csv", "text/csv")

# 📎 Footer
st.markdown("""
<hr>
<center>
    <small style="color: #888;">
        Sentilytics • Powered by Python, Streamlit, TextBlob, Plotly & WordCloud
    </small>
</center>
""", unsafe_allow_html=True)


