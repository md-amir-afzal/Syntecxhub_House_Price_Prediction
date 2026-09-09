# MediCare AI 🇮🇳

A mobile-first AI health triage prototype designed for India, including Hindi, English and Hinglish interactions and a voice-first experience.

> ⚠️ **Medical safety:** MediCare AI is an educational and triage tool, not a doctor. It cannot diagnose disease or prescribe treatment. For emergencies or serious symptoms, seek immediate professional medical care.

## What is included

- React Native + Expo Android/iOS mobile app
- India-first, large-text, low-complexity UI
- Hindi / English / Hinglish symptom entry
- Voice recording + server-side transcription integration
- AI triage API with structured JSON output
- Emergency/red-flag safety layer that runs before remote AI analysis
- Four risk levels: Low, Moderate, High, Emergency
- Conservative OTC policy: no autonomous prescription and no personalized dosing
- Optional visible-symptom photo attachment
- AI follow-up chat
- Assessment history
- Emergency help with India 112 shortcut
- JWT authentication API
- SQLite prototype database with upgrade path to PostgreSQL
- Automated emergency safety tests
- `.env` based secrets; no API keys in the mobile client

## Architecture

```text
Mobile App (Expo / React Native)
        |
        | HTTPS JSON / multipart
        v
FastAPI Backend
  |       |        |
  |       |        +--> Emergency Safety Layer
  |       +-----------> AI Provider (server-side key)
  +-------------------> SQLite prototype DB
```

## Run backend

```bash
cd backend
python -m venv .venv
# Windows: .venv\\Scripts\\activate
# macOS/Linux: source .venv/bin/activate
pip install -r requirements.txt
copy .env.example .env   # Windows
# cp .env.example .env   # macOS/Linux
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

If no AI key is configured, the API uses a deliberately limited demo triage engine so the app can be tested without an external provider.

## Run mobile app

```bash
cd mobile
npm install
npx expo start
```

For Android emulator the default backend URL is `http://10.0.2.2:8000`.
For a physical phone, set `EXPO_PUBLIC_API_URL` in `mobile/.env` to your computer's LAN IP, for example `http://192.168.1.5:8000`.

## Android build

For a development device:

```bash
npx expo run:android
```

For store-ready builds, configure an Expo/EAS project and build an AAB after validating the clinical safety, privacy, consent, and infrastructure requirements.

## Safety design

1. Validate incoming data.
2. Run deterministic emergency pattern detection.
3. If emergency is detected, return the emergency message and suppress routine OTC/self-care advice.
4. Otherwise call the AI provider, if configured.
5. Validate/normalize the structured response.
6. Run the safety layer again before rendering it to the patient.

The prototype intentionally does **not** autonomously prescribe prescription medicines. OTC content is empty by default and should only be enabled after a more comprehensive medication-safety/interaction service is validated.

## Test

```bash
cd backend
python -m pytest -q
```

## Production clinical validation required

This repository is a prototype, not a certified medical device. Before real-world clinical use, qualified healthcare professionals and appropriate legal/privacy/security specialists must validate the triage logic, emergency escalation, language behavior, medication policy, data retention, consent, and applicable Indian regulatory requirements.
