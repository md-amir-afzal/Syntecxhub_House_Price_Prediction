import json
import httpx
from .config import settings
from .safety import apply_safety, detect_emergency
from .schemas import Analysis

SYSTEM_PROMPT = """You are MediCare AI, a cautious health triage assistant for India. You are not a doctor. Never diagnose with certainty, never prescribe prescription medicines, and never advise delaying emergency care. Use simple language matching Hindi, English or Hinglish. Ask for missing critical information. OTC information is general only and must be conservative; never give personalized dosing. Do not include OTC information when key safety information is missing. Return ONLY valid JSON with keys: summary, possible_conditions, risk_level, red_flags, recommended_action, self_care, otc_information, doctor_required, emergency, follow_up_questions, safety_note. risk_level must be Low Risk, Moderate Risk, High Risk or Emergency. possible_conditions should contain 2-4 cautious possibilities, not definitive diagnoses."""


def demo_analysis(data: dict) -> dict:
    symptoms = data["symptoms"]
    text = symptoms.lower()
    flags = detect_emergency(symptoms)
    if flags:
        result = {
            "summary": f"Aapne bataya: {symptoms}",
            "possible_conditions": [],
            "risk_level": "Emergency",
            "red_flags": flags,
            "recommended_action": "Seek emergency medical care now.",
            "self_care": [],
            "otc_information": [],
            "doctor_required": True,
            "emergency": True,
            "follow_up_questions": [],
            "safety_note": "Emergency warning overrides routine self-care advice.",
        }
        return apply_safety(result, symptoms)

    fever = data.get("temperature_c") is not None and data["temperature_c"] >= 38
    severity = data["severity"]
    respiratory = any(k in text for k in ["cough", "khansi", "खांसी", "sore throat", "gala dard", "गला दर्द"])
    possible = [
        "A common viral illness may be one possibility.",
        "Another infection affecting the reported body area is another possibility.",
    ]
    if respiratory:
        possible.append("A respiratory infection is another possibility.")
    possible.append("A non-infectious cause may also explain some symptoms.")
    possible = possible[:4]
    risk = "High Risk" if severity >= 8 else "Moderate Risk" if fever or severity >= 6 else "Low Risk"
    missing = []
    if not data.get("duration") or data["duration"] == "unknown":
        missing.append("Symptoms kitne time se hain?")
    if data.get("temperature_c") is None and fever is False:
        missing.append("Agar possible ho to temperature check karke batayein.")
    result = {
        "summary": f"Aapne {data['duration']} se {symptoms} bataya hai. Severity {severity}/10 hai.",
        "possible_conditions": possible,
        "risk_level": risk,
        "red_flags": [],
        "recommended_action": "Monitor symptoms at home and seek professional care if they persist, worsen, or warning signs appear.",
        "self_care": [
            "Rest and drink enough fluids if you can safely do so.",
            "Track temperature and whether symptoms are improving or worsening.",
            "Avoid medicines that have caused an allergic reaction before.",
        ],
        "otc_information": [],
        "doctor_required": risk in {"Moderate Risk", "High Risk"},
        "emergency": False,
        "follow_up_questions": missing + [
            "Kya saans lene mein dikkat, chest pain, behoshi, severe bleeding ya confusion hai?"
        ],
        "safety_note": "Possible causes are not a diagnosis. A qualified clinician can assess you properly.",
    }
    return apply_safety(result, symptoms)


async def analyze(data: dict) -> dict:
    # Safety-first: emergency patterns are checked before any remote AI call.
    if detect_emergency(data["symptoms"]):
        return demo_analysis(data)
    if not settings.ai_api_key:
        return demo_analysis(data)

    payload = {
        "model": settings.ai_model,
        "temperature": 0.1,
        "messages": [
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": json.dumps(data, ensure_ascii=False)},
        ],
        "response_format": {"type": "json_object"},
    }
    headers = {"Authorization": f"Bearer {settings.ai_api_key}", "Content-Type": "application/json"}
    try:
        async with httpx.AsyncClient(timeout=45) as client:
            response = await client.post(
                f"{settings.ai_api_base_url.rstrip('/')}/chat/completions",
                headers=headers,
                json=payload,
            )
            response.raise_for_status()
            result = json.loads(response.json()["choices"][0]["message"]["content"])
        result = apply_safety(result, data["symptoms"])
        return Analysis.model_validate(result).model_dump()
    except Exception:
        # Fail safe: a provider outage or malformed model response must not become
        # an unsafe empty answer. Fall back to deterministic conservative triage.
        return demo_analysis(data)
