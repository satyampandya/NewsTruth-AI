# train_model.py
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score
import joblib
import os

# Load data
df_fake = pd.read_csv("data/Fake.csv")
df_true = pd.read_csv("data/True.csv")

# Add labels
df_fake["label"] = "fake"
df_true["label"] = "real"

# Combine and shuffle
df = pd.concat([df_fake, df_true])
df = df[["title", "label"]].dropna()
df = df.sample(frac=1).reset_index(drop=True)

# Convert text to numbers (TF-IDF)
vectorizer = TfidfVectorizer(stop_words="english", max_df=0.7)
X = vectorizer.fit_transform(df["title"])

# Convert labels
y = df["label"].map({"fake": 0, "real": 1})

# Split data
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Train model
model = LogisticRegression()
model.fit(X_train, y_train)

# Test accuracy
y_pred = model.predict(X_test)
accuracy = accuracy_score(y_test, y_pred)
print(f"✅ Model trained with {accuracy * 100:.2f}% accuracy.")

# Save model and vectorizer
os.makedirs("model", exist_ok=True)
joblib.dump(model, "model/fake_news_model.pkl")
joblib.dump(vectorizer, "model/vectorizer.pkl")
