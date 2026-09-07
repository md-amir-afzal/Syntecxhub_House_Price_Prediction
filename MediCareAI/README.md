# MediCare AI

A mobile-first AI health triage prototype designed for India, including Hindi, English and Hinglish interactions and a voice-first experience.

> ⚠️ **Medical safety:** MediCare AI is an educational and triage tool, not a doctor. It cannot diagnose disease or prescribe treatment. For emergencies or serious symptoms, seek immediate professional medical care.

## What is included

- React Native + Expo Android/iOS mobile app
- India-first, large-text, low-complexity UI
- Hindi / English / Hinglish symptom entry
- Voice recording + server-side transcription integration
- AI triage API with structured JSON output
- Emergency/red-flag safety layer before remote AI analysis
- Four risk levels: Low, Moderate, High, Emergency
- Conservative OTC policy: no autonomous prescription and no personalized dosing
- Optional visible-symptom photo attachment
- AI follow-up chat
- Assessment history
- Emergency help with India 112 shortcut
- JWT authentication API
- SQLite prototype database
- Automated emergency safety tests
- `.env` based secrets; no API keys in the mobile client

## Run backend

```bash
cd backend
python -m venv .venv
pip install -r requirements.txt
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

If no AI key is configured, the API uses a limited demo triage engine for local testing.

## Run mobile

```bash
cd mobile
npm install
npx expo start
```

Android emulator default: `http://10.0.2.2:8000`. For a physical phone, set `EXPO_PUBLIC_API_URL` to your computer's LAN IP.

## Safety design

1. Validate incoming data.
2. Run deterministic emergency detection.
3. If emergency is detected, suppress routine OTC/self-care advice.
4. Otherwise call the server-side AI provider if configured.
5. Validate and safety-filter the structured response.
6. Render patient-friendly results.

## Production validation

This is a prototype, not a certified medical device. Qualified healthcare professionals and appropriate legal/privacy/security specialists must validate the triage logic, emergency escalation, language behavior, medication policy, consent, retention, and applicable Indian requirements before real-world clinical use.
