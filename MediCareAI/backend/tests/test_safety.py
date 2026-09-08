from app.safety import detect_emergency


def test_normal_symptoms_are_not_emergency():
    assert detect_emergency("fever and cough") == []


def test_chest_pain_is_emergency():
    flags = detect_emergency("severe chest pain")
    assert "chest pain/pressure" in flags


def test_chest_pain_with_breathing_difficulty_detects_both():
    flags = detect_emergency("severe chest pain and difficulty breathing")
    assert "chest pain/pressure" in flags
    assert "severe breathing difficulty" in flags


def test_hinglish_emergency_is_detected():
    flags = detect_emergency("saans lene mein bahut dikkat aur seene mein dard")
    assert "severe breathing difficulty" in flags
    assert "chest pain/pressure" in flags
