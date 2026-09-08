import re

EMERGENCY_PATTERNS = {
    "chest pain/pressure": r"(?:chest\s*(?:pain|pressure)|seene?\s*(?:me|mein)\s*dard|सीने\s*में\s*(?:दर्द|दबाव))",
    "severe breathing difficulty": r"(?:can't\s*breathe|cannot\s*breathe|severe\s*breathing(?:\s*difficulty)?|difficulty\s*breathing|breathing\s*difficulty|breath(?:ing)?\s*(?:is\s*)?(?:very\s*)?difficult|saans\s*(?:nahi|nahin)\s*(?:aa|le)|saans\s*lene\s*(?:mein|me)\s*(?:mushkil|dikkat)|सांस\s*(?:नहीं|बहुत)\s*(?:आ|ले)|सांस\s*लेने\s*(?:में|मे)\s*(?:मुश्किल|दिक्कत))",
    "stroke-like symptoms": r"(?:face\s*droop|slurred\s*speech|speech\s*(?:problem|difficulty)|one\s*side\s*(?:weak|numb)|ek\s*taraf\s*(?:kamzor|sun)|मुंह\s*(?:टेढ़ा|एक\s*तरफ)|बोलने\s*(?:में|मे)\s*दिक्कत|एक\s*तरफ\s*(?:कमजोर|सुन्न))",
    "loss of consciousness": r"(?:unconscious|passed\s*out|fainted|बेहोश|hosh\s*(?:nahi|nahin))",
    "severe bleeding": r"(?:severe\s*bleeding|bleeding\s*(?:won't|will\s*not)\s*stop|bahut\s*(?:khoon|blood)|बहुत\s*(?:खून|रक्त))",
    "seizure": r"(?:seizure|convulsion|fit\s*(?:aa|aaya)|दौरा|मिर्गी\s*का\s*दौरा)",
    "severe allergic reaction": r"(?:anaphylaxis|throat\s*swelling|face\s*swelling\s*(?:and|&)\s*breath|gala\s*(?:suj|sooj)|गला\s*(?:सूज|सूजन))",
    "severe poisoning": r"(?:poisoning|poison\s*(?:drink|taken)|overdose|zehar|ज़हर|विषाक्तता|ओवरडोज)",
    "sudden severe headache": r"(?:worst\s*headache|sudden\s*severe\s*headache|achanak\s*(?:bahut|tez)\s*sir\s*dard|अचानक\s*(?:बहुत|तेज)\s*सिरदर्द)",
    "severe abdominal pain": r"(?:severe\s*abdominal\s*pain|severe\s*stomach\s*pain|pet\s*(?:mein|me)\s*bahut\s*dard|पेट\s*(?:में|मे)\s*बहुत\s*dard|पेट\s*(?:में|मे)\s*बहुत\s*दर्द)",
    "self-harm emergency": r"(?:suicide|suicidal|kill\s*myself|self\s*harm|khudkushi|khud\s*ko\s*(?:nuksan|mar)|आत्महत्या|खुद\s*को\s*(?:नुकसान|मार))",
}

EMERGENCY_MESSAGE = "⚠️ This may be a medical emergency. Do not rely on this AI assessment. Contact your local emergency service or go to the nearest emergency department immediately."


def detect_emergency(text: str) -> list[str]:
    text = text or ""
    return [name for name, pattern in EMERGENCY_PATTERNS.items() if re.search(pattern, text, re.I)]


def apply_safety(analysis: dict, source_text: str) -> dict:
    flags = detect_emergency(source_text)
    if flags:
        analysis.update(
            {
                "risk_level": "Emergency",
                "emergency": True,
                "doctor_required": True,
                "red_flags": flags,
                "recommended_action": EMERGENCY_MESSAGE,
                "otc_information": [],
                "self_care": ["Do not delay emergency medical care."],
                "safety_note": "Emergency warning overrides routine self-care advice.",
            }
        )
    else:
        analysis["emergency"] = False
        analysis.setdefault("red_flags", [])
        analysis.setdefault(
            "safety_note",
            "Educational triage information only. This is not a diagnosis or prescription.",
        )
    return analysis
