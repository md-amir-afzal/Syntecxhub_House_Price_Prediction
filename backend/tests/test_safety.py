from app.safety import detect_emergency

def test_chest_pain(): assert detect_emergency("I have severe chest pain and pressure")
def test_hinglish_breathing(): assert detect_emergency("meri saans nahi aa rahi")
def test_hindi_stroke(): assert detect_emergency("मुंह टेढ़ा हो गया और बोलने में दिक्कत है")
def test_routine_symptom(): assert not detect_emergency("mild cough for two days")


def test_poisoning(): assert detect_emergency("I think I took an overdose")
def test_self_harm(): assert detect_emergency("I want to kill myself")
def test_no_false_positive_for_mild_headache(): assert not detect_emergency("mild headache since yesterday")
def test_multiple_flags():
    flags = detect_emergency("severe chest pain and cannot breathe")
    assert "chest pain/pressure" in flags and "severe breathing difficulty" in flags
