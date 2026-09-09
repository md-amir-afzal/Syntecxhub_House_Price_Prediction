from fastapi import FastAPI,HTTPException,Depends,Header,UploadFile,File
from fastapi.middleware.cors import CORSMiddleware
from .schemas import AssessmentIn,AuthIn,TokenOut,ChatIn,Analysis
from .ai import analyze,chat_reply
from .safety import detect_emergency,EMERGENCY_MESSAGE
from .db import init_db,save_assessment,create_user,get_user,get_history
from .auth import hash_password,verify_password,create_access_token,get_user_id_from_token
from .config import settings
app=FastAPI(title='MediCare AI API',version='0.3.0');app.add_middleware(CORSMiddleware,allow_origins=[x.strip() for x in settings.cors_origins.split(',') if x.strip()],allow_credentials=True,allow_methods=['*'],allow_headers=['*']);init_db()
@app.get('/health')
def health():return {'status':'ok','service':'MediCare AI','prototype':True}
@app.post('/api/v1/auth/register',response_model=TokenOut)
def register(payload:AuthIn):
    if get_user(payload.email):raise HTTPException(409,'An account with this email already exists.')
    return TokenOut(access_token=create_access_token(create_user(payload.email,hash_password(payload.password))))
@app.post('/api/v1/auth/login',response_model=TokenOut)
def login(payload:AuthIn):
    user=get_user(payload.email)
    if not user or not verify_password(payload.password,user['password_hash']):raise HTTPException(401,'Invalid email or password.')
    return TokenOut(access_token=create_access_token(user['id']))
def current_user(authorization:str|None=Header(default=None))->int:
    if not authorization or not authorization.lower().startswith('bearer '):raise HTTPException(401,'Please log in to access your health assessments.')
    user_id=get_user_id_from_token(authorization.split(' ',1)[1].strip())
    if not user_id:raise HTTPException(401,'Your session is invalid or expired. Please log in again.')
    return user_id
@app.post('/api/v1/assessments/analyze',response_model=Analysis)
async def assessment(payload:AssessmentIn,user_id:int=Depends(current_user)):
    data=payload.model_dump()
    try:
        result=Analysis.model_validate(await analyze(data));save_assessment(user_id,data,result.model_dump());return result
    except Exception:raise HTTPException(502,'AI service unavailable. Please try again. If symptoms are serious, seek professional care.')
@app.get('/api/v1/assessments/history')
def history(user_id:int=Depends(current_user)):return {'items':get_history(user_id)}
@app.post('/api/v1/safety/emergency-check')
def emergency_check(symptoms:str):
    flags=detect_emergency(symptoms);return {'emergency':bool(flags),'red_flags':flags,'message':EMERGENCY_MESSAGE if flags else None}
@app.post('/api/v1/chat')
async def chat(payload:ChatIn,user_id:int=Depends(current_user)):
    flags=detect_emergency(payload.message)
    if flags:return {'emergency':True,'red_flags':flags,'reply':EMERGENCY_MESSAGE}
    return {'emergency':False,'red_flags':[],'reply':await chat_reply(payload.message,payload.language,payload.context)}
@app.post('/api/v1/voice/transcribe')
async def transcribe_voice(audio:UploadFile=File(...),user_id:int=Depends(current_user)):
    if not settings.ai_api_key:raise HTTPException(503,'Voice transcription is not configured. Add AI_API_KEY on the backend.')
    raw=await audio.read()
    if len(raw)>10*1024*1024:raise HTTPException(413,'Audio file is too large. Please record a shorter message.')
    try:
        import httpx
        headers={'Authorization':f'Bearer {settings.ai_api_key}'};files={'file':(audio.filename or 'symptoms.m4a',raw,audio.content_type or 'audio/mp4')};data={'model':'gpt-4o-mini-transcribe','language':'hi'}
        async with httpx.AsyncClient(timeout=60) as client:r=await client.post(f"{settings.ai_api_base_url.rstrip('/')}/audio/transcriptions",headers=headers,files=files,data=data)
        r.raise_for_status();return {'text':r.json().get('text','')}
    except Exception:raise HTTPException(502,'Voice transcription failed. Please type your symptoms instead.')
