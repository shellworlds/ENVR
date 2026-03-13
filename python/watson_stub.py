# SN-112BA: IBM Watson integration stub. Main developer: shellworlds.
"""Stub for Watson NLU/Assistant; replace with ibm-watson when credentials set."""

from typing import Dict, Any


def watson_nlu_analyze(text: str) -> Dict[str, Any]:
    return {
        "sentiment": {"score": 0.0, "label": "neutral"},
        "keywords": [],
        "stub": True,
        "message": "SN-112BA Watson stub; set WATSON_URL and API key for live.",
    }


def watson_assistant_message(session_id: str, input_text: str) -> Dict[str, Any]:
    return {
        "output": {"generic": [{"response_type": "text", "text": "SN-112BA stub response."}]},
        "session_id": session_id,
        "stub": True,
    }


if __name__ == "__main__":
    print(watson_nlu_analyze("Sample text"))
