from fastapi import Depends,FastAPI,File,Header,HTTPException,UploadFile
from fastapi.middleware.cors import CORSMiddleware
import httpx
from .ai import analyze
from .auth import create_token,get_user_id,hash_password,verify_password
from .config import settings
from .db import create_user,get_user,init_db,list_assessments,save_assessment
from .safety import detect_emergency,EMERGENCY_MESSAGE
from .schemas import Analysis,AssessmentIn,ChatIn,LoginIn,RegisterIn
app=FastAPI(title='MediCare AI API',version='1.0.0'); app.add_middleware(CORSMiddleware,allow_origins=settings.cors_list,allow_credentials=True,allow_methods=['*'],allow_headers=['*']); init_db()
def current_user(authorization:str|None=Header(default=None)):
 if not authorization or not authorization.lower().startswith('bearer '): return 0
 return get_user_id(authorization.split(' ',1)[1]) or 0
@app.get('/health')
def health(): return {'status':'ok','service':'MediCare AI','prototype':True}
@app.post('/api/v1/auth/register')
def register(payload:RegisterIn):
 if get_user(payload.email): raise HTTPException(409,'An account with this email already exists.')
 return {'access_token':create_token(create_user(payload.email,hash_password(payload.password))),'token_type':'bearer'}
@app.post('/api/v1/auth/login')
def login(payload:LoginIn):
 u=get_user(payload.email)
 if not u or not verify_password(payload.password,u['password_hash']): raise HTTPException(401,'Invalid email or password.')
 return {'access_token':create_token(u['id']),'token_type':'bearer'}
@app.post('/api/v1/assessments/analyze',response_model=Analysis)
async def assessment(payload:AssessmentIn,user_id:int=Depends(current_user)):
 try:
  data=payload.model_dump(); result=await analyze(data); save_assessment(user_id,data,result); return result
 except Exception: raise HTTPException(502,'AI service unavailable. Please try again or seek professional care if symptoms are serious.')
@app.get('/api/v1/assessments/history')
def history(user_id:int=Depends(current_user)): return {'items':list_assessments(user_id)}
@app.post('/api/v1/safety/emergency-check')
def emergency_check(symptoms:str):
 flags=detect_emergency(symptoms); return {'emergency':bool(flags),'red_flags':flags,'message':EMERGENCY_MESSAGE if flags else None}
@app.post('/api/v1/chat')
async def chat(payload:ChatIn):
 flags=detect_emergency(payload.message)
 if flags: return {'reply':EMERGENCY_MESSAGE,'emergency':True,'red_flags':flags,'follow_up_questions':[]}
 return {'reply':'Samajh gaya. Main diagnosis nahi karunga. Pehle symptoms kab se hain, severity 1–10 kitni hai, aur kya saans ki dikkat, chest pain, behoshi, severe bleeding ya confusion hai?','emergency':False,'red_flags':[],'follow_up_questions':['Symptoms kab se hain?','Severity 1–10 kitni hai?','Kya breathing problem, chest pain, fainting ya severe bleeding hai?']}
@app.post('/api/v1/voice/transcribe')
async def transcribe_voice(file:UploadFile=File(...)):
 if not settings.ai_api_key: raise HTTPException(503,'Voice transcription is not configured on this server.')
 if file.content_type and not file.content_type.startswith('audio/'): raise HTTPException(400,'Please upload an audio recording.')
 raw=await file.read()
 if len(raw)>10*1024*1024: raise HTTPException(413,'Audio file is too large.')
 try:
  async with httpx.AsyncClient(timeout=60) as client:
   r=await client.post(f"{settings.ai_api_base_url.rstrip('/')}/audio/transcriptions",headers={'Authorization':f'Bearer {settings.ai_api_key}'},data={'model':'gpt-4o-mini-transcribe'},files={'file':(file.filename or 'symptoms.m4a',raw,file.content_type or 'audio/m4a')}); r.raise_for_status(); return {'text':r.json().get('text','')}
 except Exception: raise HTTPException(502,'Voice transcription service unavailable. Please type your symptoms instead.')
