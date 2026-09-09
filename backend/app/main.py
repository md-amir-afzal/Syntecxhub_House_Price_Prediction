from fastapi import Depends, FastAPI, File, Header, HTTPException, UploadFile
import httpx
from fastapi.middleware.cors import CORSMiddleware
from .ai import analyze
from .auth import create_token, get_user_id, hash_password, verify_password
from .config import settings
from .db import create_user, get_user, init_db, list_assessments, save_assessment
from .safety import detect_emergency, EMERGENCY_MESSAGE
from .schemas import Analysis, AssessmentIn, ChatIn, LoginIn, RegisterIn

app = FastAPI(title="MediCare AI API", version="1.0.0", description="Safety-first health triage prototype for India")
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_list,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
init_db()


def current_user(authorization: str | None = Header(default=None)) -> int:
    if not authorization or not authorization.lower().startswith("bearer "):
        raise HTTPException(status_code=401, detail="Please log in to access your health assessments.")
    user_id = get_user_id(authorization.split(" ", 1)[1])
    if not user_id:
        raise HTTPException(status_code=401, detail="Your session is invalid or expired. Please log in again.")
    return user_id


@app.get("/health")
def health():
    return {"status": "ok", "service": "MediCare AI", "prototype": True}


@app.post("/api/v1/auth/register")
def register(payload: RegisterIn):
    if get_user(payload.email):
        raise HTTPException(status_code=409, detail="An account with this email already exists.")
    try:
        user_id = create_user(payload.email, hash_password(payload.password))
    except Exception:
        raise HTTPException(status_code=409, detail="Unable to create account.")
    return {"access_token": create_token(user_id), "token_type": "bearer"}


@app.post("/api/v1/auth/login")
def login(payload: LoginIn):
    user = get_user(payload.email)
    if not user or not verify_password(payload.password, user["password_hash"]):
        raise HTTPException(status_code=401, detail="Invalid email or password.")
    return {"access_token": create_token(user["id"]), "token_type": "bearer"}


@app.post("/api/v1/assessments/analyze", response_model=Analysis)
async def assessment(payload: AssessmentIn, user_id: int = Depends(current_user)):
    data = payload.model_dump()
    try:
        result = await analyze(data)
        result = Analysis.model_validate(result).model_dump()
        save_assessment(user_id, data, result)
        return result
    except Exception:
        raise HTTPException(
            status_code=502,
            detail="AI service unavailable. Please try again or seek professional care if symptoms are serious.",
        )


@app.get("/api/v1/assessments/history")
def history(user_id: int = Depends(current_user)):
    return {"items": list_assessments(user_id)}


@app.post("/api/v1/safety/emergency-check")
def emergency_check(symptoms: str):
    flags = detect_emergency(symptoms)
    return {"emergency": bool(flags), "red_flags": flags, "message": EMERGENCY_MESSAGE if flags else None}


@app.post("/api/v1/chat")
async def chat(payload: ChatIn):
    flags = detect_emergency(payload.message)
    if flags:
        return {
            "reply": EMERGENCY_MESSAGE,
            "emergency": True,
            "red_flags": flags,
            "follow_up_questions": [],
        }
    return {
        "reply": "Samajh gaya. Main diagnosis nahi karunga. Pehle symptoms kab se hain, severity 1–10 kitni hai, aur kya saans ki dikkat, chest pain, behoshi, severe bleeding ya confusion hai?",
        "emergency": False,
        "red_flags": [],
        "follow_up_questions": [
            "Symptoms kab se hain?",
            "Severity 1–10 kitni hai?",
            "Kya breathing problem, chest pain, fainting ya severe bleeding hai?",
        ],
    }


@app.post("/api/v1/voice/transcribe")
async def transcribe_voice(file: UploadFile = File(...)):
    """Transcribe short symptom audio through the server-side AI provider.
    API keys never leave the backend. A real provider key is required for this endpoint.
    """
    if not settings.ai_api_key:
        raise HTTPException(status_code=503, detail="Voice transcription is not configured on this server.")
    if file.content_type and not file.content_type.startswith("audio/"):
        raise HTTPException(status_code=400, detail="Please upload an audio recording.")
    raw = await file.read()
    if len(raw) > 10 * 1024 * 1024:
        raise HTTPException(status_code=413, detail="Audio file is too large.")
    headers = {"Authorization": f"Bearer {settings.ai_api_key}"}
    files = {"file": (file.filename or "symptoms.m4a", raw, file.content_type or "audio/m4a")}
    data = {"model": "gpt-4o-mini-transcribe", "prompt": "Medical symptom conversation. Preserve Hindi, English and Hinglish words accurately."}
    try:
        async with httpx.AsyncClient(timeout=60) as client:
            response = await client.post(f"{settings.ai_api_base_url.rstrip('/')}/audio/transcriptions", headers=headers, data=data, files=files)
            response.raise_for_status()
            return {"text": response.json().get("text", "")}
    except Exception:
        raise HTTPException(status_code=502, detail="Voice transcription service unavailable. Please type your symptoms instead.")
