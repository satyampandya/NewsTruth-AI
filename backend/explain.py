# backend/explain.py
import numpy as np

def get_top_contributing_words(text, vectorizer, model, top_n=5):
    tfidf_vector = vectorizer.transform([text])
    feature_names = np.array(vectorizer.get_feature_names_out())
    weights = model.coef_[0]
    word_scores = tfidf_vector.multiply(weights).toarray()[0]
    top_indices = word_scores.argsort()[-top_n:][::-1]
    return list(zip(feature_names[top_indices], word_scores[top_indices]))
