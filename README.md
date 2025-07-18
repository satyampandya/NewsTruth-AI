
# 📰 NewsTruth-AI

**NewsTruth-AI** is a smart fake news detection system built with a **hybrid AI architecture**. It combines Machine Learning and Google’s Gemini AI (LLM) to analyze news headlines and content. The system delivers accurate judgments, credibility analysis, and easy-to-understand insights in real-time — all in a clean Streamlit interface.

🎯 **Try it Live:** [newstruth-ai.streamlit.app](https://newstruth-ai.streamlit.app/)

---

## 🚀 Features

- ✅ Detects fake, real, or biased news using combined AI power
- 🧠 Gemini 2.5 Flash gives reasoning, bias detection & summary
- 📊 ML model extracts tone, confidence & keyword influence
- 🔄 Hybrid logic prioritizes best judgment using both systems
- 📎 Clean Streamlit UI with responsive design
- 🌍 Aligned with UN SDG Goal 16: Peace, Justice and Strong Institutions

---

## 🧠 Technologies Used

- **Frontend:** Streamlit
- **Machine Learning:** Scikit-learn, Logistic Regression, TfidfVectorizer
- **LLM Integration:** Gemini 2.5 Flash via Google API
- **Visualization:** Altair
- **Others:** joblib, dotenv, requests, Python 3.10+

---

## 📂 Project Structure

```
📁 NewsTruth-AI/
├── app.py                     # Streamlit UI
├── train_model.py             # ML training script
├── model/
│   └── fake_news_model.pkl, vectorizer.pkl
├── data/
│   └── Fake.csv, True.csv
├── backend/
│   ├── explain.py             # Extract word influence
│   ├── fusion.py              # Final decision logic
│   └── gemini_engine.py       # Gemini API integration
├── .env                       # Environment secrets (ignored)
├── .gitignore
├── requirements.txt
└── README.md
```

---

## 🧪 How to Run Locally

> You need Python 3.10+ installed.

1. **Clone the repository**
   ```bash
   git clone https://github.com/satyampandya/NewsTruth-AI.git
   cd NewsTruth-AI
   ```

2. **Create virtual environment**
   ```bash
   python -m venv venv
   ```

3. **Activate it**
   - Windows:
     ```bash
     venv\Scripts\activate
     ```
   - macOS/Linux:
     ```bash
     source venv/bin/activate
     ```

4. **Install all requirements**
   ```bash
   pip install -r requirements.txt
   ```

5. **Create `.env` file in root with this:**
   ```env
   GEMINI_API_KEY=your_gemini_api_key_here
   ```

6. **Run the app**
   ```bash
   streamlit run app.py
   ```

---

## 🌐 Deployment

This project is deployed for free using **Streamlit Cloud**.

🔗 **Live App:** [https://newstruth-ai.streamlit.app](https://newstruth-ai.streamlit.app)

---

## 🎯 UN SDG Alignment

NewsTruth supports **Goal 16** of the UN Sustainable Development Goals:

> _“Ensure public access to information and protect fundamental freedoms.”_

It empowers individuals to identify fake news and promotes truthful, unbiased media.

---

## 👨‍💻 Author

- **👤 Name:** Satyam Pandya  
- **📚 Project Type:** Individual Internship Project  
- **🎓 Platform:** IBM SkillBuild Internship  
- **🗓️ Year:** 2025

---

## ⚠️ Limitations

| Engine      | Limitation                                         |
|-------------|-----------------------------------------------------|
| Gemini AI   | May struggle with satire or vague text             |
| ML Model    | Trained on short English headlines only            |
| Combined AI | ⚠️ Always verify highly sensitive or viral news   |

---

## 📬 License

This project is free for learning and research purposes.  
Please do not misuse the model or system for misinformation.

---
