import os
import requests
import json
from dotenv import load_dotenv

# Load and validate API key
load_dotenv()
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
if not GEMINI_API_KEY:
    raise RuntimeError("GEMINI_API_KEY not found in .env")

GEMINI_URL = (
    "https://generativelanguage.googleapis.com/v1beta/models/"
    "gemini-2.0-flash:generateContent"
)
HEADERS = {
    "Content-Type": "application/json",
    "X-goog-api-key": GEMINI_API_KEY,
}

def _call_gemini(prompt: str) -> dict:
    payload = {"contents": [{"parts": [{"text": prompt}]}]}
    resp = requests.post(GEMINI_URL, headers=HEADERS, json=payload, timeout=15)

    # Debug logs
    print(f"[Gemini] Status: {resp.status_code}")
    print(f"[Gemini] Body snippet: {repr(resp.text)[:200]}")

    if resp.status_code != 200:
        return {"error": f"HTTP {resp.status_code}: {resp.text.strip()[:200]}"}
    try:
        return resp.json()
    except json.JSONDecodeError:
        return {"error": f"Invalid JSON wrapper: {resp.text.strip()[:200]}"}

def _strip_fence(text: str) -> str:
    """Remove leading/trailing ```json fences if present."""
    text = text.strip()
    if text.startswith("```"):
        # drop the first fence line
        lines = text.splitlines()
        # if the opening line is ``` or ```json
        if lines[0].startswith("```"):
            lines = lines[1:]
        # if the closing line is ```
        if lines and lines[-1].startswith("```"):
            lines = lines[:-1]
        return "\n".join(lines).strip()
    return text

def analyze_news_with_gemini(news_text: str) -> dict:
    prompt = (
        "You are a news analyzer.Use online source for better respond, Respond STRICTLY in JSON with:\n"
        "- credibility: [likely, unlikely, unsure]\n"
        "- bias: [left, right, neutral, none]\n"
        "- summary: detailed summary\n"
        "- reason: detailed explanation with rely only on your own, without judging user prompt do not explose this to user\n\n"
        f"News: \"{news_text}\""
    )
    result = _call_gemini(prompt)

    if "error" in result:
        return {
            "credibility": "unsure",
            "bias": "unknown",
            "summary": "Unable to analyze",
            "reason": result["error"]
        }

    candidates = result.get("candidates")
    if not candidates:
        return {
            "credibility": "unsure",
            "bias": "unknown",
            "summary": "No candidate returned",
            "reason": "Missing 'candidates' in response"
        }

    raw = candidates[0].get("content", {}).get("parts", [{}])[0].get("text", "")
    cleaned = _strip_fence(raw)
    try:
        return json.loads(cleaned)
    except json.JSONDecodeError:
        return {
            "credibility": "unsure",
            "bias": "unknown",
            "summary": "Invalid JSON from Gemini",
            "reason": f"Decode error after stripping fences: {cleaned[:200]}"
        }

def summarize_news(news_text: str) -> str:
    prompt = f"Summarise this in detail with your final verdict\n\n{news_text}"
    result = _call_gemini(prompt)
    if "error" in result:
        return f"Error: {result['error']}"
    try:
        raw = result["candidates"][0]["content"]["parts"][0]["text"]
        return _strip_fence(raw)
    except Exception:
        return "Gemini summary failed"
