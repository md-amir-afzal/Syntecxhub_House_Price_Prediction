from app.safety import detect_emergency
def test_chest_pain():assert detect_emergency('I have severe chest pain and pressure')
def test_hinglish_breathing():assert detect_emergency('meri saans nahi aa rahi')
def test_hindi_stroke():assert detect_emergency('मुंह टेढ़ा हो गया और बोलने में दिक्कत है')
def test_routine_symptom():assert not detect_emergency('mild cough for two days')
