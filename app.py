import streamlit as st
import joblib
import pandas as pd
import altair as alt
from backend.explain import get_top_contributing_words
from backend.gemini_engine import analyze_news_with_gemini
from backend.fusion import hybrid_decision

# Load model and vectorizer
model = joblib.load("model/fake_news_model.pkl")
vectorizer = joblib.load("model/vectorizer.pkl")

# Page Config
st.set_page_config(page_title="NewsTruth - Fight Fake News", page_icon="📰", layout="centered")

# Sidebar Content
with st.sidebar:
    st.markdown("## 📰 NewsTruth")
    st.markdown("**AI-powered fake news detection system**")

    st.markdown("### 🌍 UN SDG Alignment")
    st.markdown("""
    NewsTruth supports **Goal 16: Peace, Justice and Strong Institutions**.
    
    > _“Ensure public access to information and protect fundamental freedoms.”_

    This project promotes **truthful media**, **digital literacy**, and **informed citizenship**.
    """)

    st.markdown("### 🛠️ How It Works")
    st.markdown("""
    - 🤖 **Gemini AI** detects bias & credibility  
    - 📊 **ML model** analyzes tone & keywords  
    - 🔄 Combined for a **smart unified verdict**
    """)

    st.markdown("### ⚠️ Limitations")
    st.markdown("""
    - **Gemini AI**
      - Version: *Gemini 2.5 Flash*
      - Knowledge cutoff: *June 2024*
      - May fail on satire or vague topics

    - **ML Model**
      - Trained on short English headlines
      - May misjudge sarcasm or partial context

    > Always verify sensitive news from trusted sources.
    """)

    st.markdown("### 💡 Tips for Best Use")
    st.markdown("""
    - Paste short headlines or summaries  
    - Avoid long articles or unclear text  
    - If result shows ⚠️ *Needs Review*, use human judgment
    """)


# Header
st.title("📢 NewsTruth")
st.caption("Promoting access to truthful and unbiased information using Hybrid AI.")

# Input Section
st.markdown("#### 📝 Enter News Headline or Content")
input_col, btn_col = st.columns([5, 1])
with input_col:
    user_input = st.text_area("", height=100, placeholder="e.g. India wins the T20 World Cup 2024")
with btn_col:
    analyze = st.button("🔍 Analyze")

# Handle input
if analyze:
    if not user_input.strip():
        st.warning("Please enter some news content to analyze.")
    else:
        with st.spinner("Analyzing with Machine Learning + Gemini AI..."):
            # ML Prediction
            X_input = vectorizer.transform([user_input])
            ml_pred = model.predict(X_input)[0]
            confidence = model.predict_proba(X_input)[0].max()
            label = "Real" if ml_pred == 1 else "Fake"
            top_words = get_top_contributing_words(user_input, vectorizer, model)

            # Gemini Analysis
            gemini_result = analyze_news_with_gemini(user_input)
            credibility = gemini_result.get("credibility", "unsure").title()
            bias = gemini_result.get("bias", "unknown").title()
            summary = gemini_result.get("summary", "No summary available.")
            reason = gemini_result.get("reason", "No explanation provided.")

            # Final Verdict
            final_verdict = hybrid_decision(label, gemini_result)

        st.markdown("---")

        # Verdict Display
        st.markdown("### ✅ Final Verdict")
        if "Fake" in final_verdict:
            st.error(final_verdict)
        elif "Real" in final_verdict:
            st.success(final_verdict)
        else:
            st.warning(final_verdict)

        # Bias
        st.markdown("### ⚖️ Bias Analysis")
        if bias.lower() in ["left", "right"]:
            st.warning(f"Detected bias: **{bias}**")
        elif bias.lower() == "neutral":
            st.success("This news appears **neutral**.")
        else:
            st.info("Bias could not be determined.")

        # Confidence
        st.markdown("### 📈 Model Confidence")
        st.markdown(f"The system is **{confidence * 100:.2f}%** confident about this prediction.")

        # Contribution Graph - Altair
        st.markdown("### 📊 Contributing Words")
        if top_words:
            df_words = pd.DataFrame(top_words, columns=["Word", "Score"])
            chart = alt.Chart(df_words).mark_bar(color='#4c78a8').encode(
                x=alt.X("Score:Q", title="Importance"),
                y=alt.Y("Word:N", sort='-x', title="Top Words")
            ).properties(height=200, width=400)
            st.altair_chart(chart, use_container_width=False)
        else:
            st.info("No contributing words found.")

        # Reason
        st.markdown("### 🧠 Reasoning")
        st.markdown(f"> {reason}")

        # Summary
        st.markdown("### 📰 Summary")
        st.info(summary)

        st.markdown("---")
        st.caption("🕊️ NewsTruth supports the UN's mission to ensure access to information and protect fundamental freedoms.")

else:
    st.info("Paste a news headline or short content and click **Analyze** to begin.")
