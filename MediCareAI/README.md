# MediCare AI

India-focused mobile-first AI health triage prototype built with **React Native + Expo Router** and a **FastAPI** backend.

## What works
- Account registration/login with JWT bearer authentication
- Authenticated assessment analysis + per-user history
- Emergency screening before routine AI guidance
- Hindi / English / Hinglish input and response design
- Native microphone recording using `expo-audio`; backend transcription integration
- AI provider integration through server-side environment variables
- Conservative structured triage output: possible causes, risk level, red flags, next step, self-care and follow-up questions
- Emergency instructions for India including 112
- Profile/privacy and logout screens

## Run backend
```bash
cd backend
python -m venv .venv
# Windows PowerShell: .\\.venv\\Scripts\\Activate.ps1
pip install -r requirements.txt
copy .env.example .env
uvicorn app.main:app --reload --port 8000
```

## Run mobile
```bash
cd mobile
npm install
npx expo start
```

For an Android emulator, `EXPO_PUBLIC_API_URL=http://10.0.2.2:8000` works. For a physical phone, use the computer's LAN IP.

## Tests / checks
```bash
PYTHONPATH=backend pytest -q backend/tests
cd mobile
npm run typecheck
npx expo-doctor
```

## Important
This is an **educational/clinical-support prototype**, not a medical device or a doctor. It must be clinically validated, security/privacy reviewed, and tested by qualified healthcare professionals before real-world clinical use.
