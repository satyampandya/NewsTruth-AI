def hybrid_decision(ml_label, gemini_info):
    credibility = gemini_info.get("credibility", "unsure").lower()
    bias = gemini_info.get("bias", "unknown").lower()

    # Rule 1: Trust Gemini if it's confident
    if credibility == "likely" and bias in ["neutral", "none"]:
        return "✅ Real & Reliable"
    elif credibility == "unlikely":
        return "❌ Fake & Misleading"

    # Rule 2: If Gemini is unsure or unknown, fallback to ML
    elif credibility == "unsure" or bias == "unknown":
        if ml_label == "Real":
            return "✅ Likely Real (based on ML tone & patterns)"
        else:
            return "❌ Likely Fake (based on ML tone & patterns)"

    # Rule 3: Partial signal (bias present, credibility missing)
    elif bias in ["left", "right"]:
        return f"⚠️ Possibly Biased ({bias.title()})"

    # Default catch
    return "⚠️ Needs Human Review"
