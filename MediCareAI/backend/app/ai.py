import json,httpx
from .config import settings
from .safety import apply_safety
SYSTEM_PROMPT='''You are MediCare AI, a cautious health triage assistant for India. You are not a doctor. Never diagnose with certainty, never prescribe prescription medicines, never advise delaying emergency care. Use simple Hindi, English or Hinglish matching the request. Ask for missing critical information. OTC information is general education only: do not give personalized dosing and do not suggest OTC medicines when key safety information is missing. Return ONLY JSON with keys summary, possible_conditions (2-4), risk_level, red_flags, recommended_action, self_care, otc_information, doctor_required, emergency, follow_up_questions, safety_note.'''
async def provider(messages,response_format=None):
    payload={"model":settings.ai_model,"temperature":0.1,"messages":messages}
    if response_format: payload['response_format']=response_format
    headers={"Authorization":f"Bearer {settings.ai_api_key}","Content-Type":"application/json"}
    async with httpx.AsyncClient(timeout=45) as client:
        r=await client.post(f"{settings.ai_api_base_url.rstrip('/')}/chat/completions",headers=headers,json=payload); r.raise_for_status(); return r.json()['choices'][0]['message']['content']
def demo_analysis(data):
    symptoms=data['symptoms']; s=symptoms.lower()
    if any(x in s for x in ['chest pain','chest pressure','seene mein dard','सीने में दर्द','saans nahi','saans lene mein bahut dikkat','बेहोश','unconscious','seizure','दौरा','severe bleeding','bahut khoon']):
        return apply_safety({"summary":f"You reported: {symptoms}","possible_conditions":[],"risk_level":"Emergency","red_flags":[],"recommended_action":"Seek emergency medical care now.","self_care":[],"otc_information":[],"doctor_required":True,"emergency":True,"follow_up_questions":[],"safety_note":"Emergency symptoms require immediate professional assessment."},symptoms)
    fever=data.get('temperature_c') is not None and data['temperature_c']>=38
    return apply_safety({"summary":f"You reported {symptoms}, severity {data['severity']}/10, for {data['duration']}.","possible_conditions":["A common viral infection","Another respiratory or local infection","A non-infectious cause related to the reported symptoms"],"risk_level":"Moderate Risk" if fever or data['severity']>=7 else "Low Risk","red_flags":[],"recommended_action":"Monitor symptoms and consider a doctor visit if symptoms persist, worsen, or new warning signs appear.","self_care":["Rest and drink enough fluids if you can safely do so.","Track temperature and symptom changes.","Avoid medicines that have caused you reactions before."],"otc_information":[],"doctor_required":bool(fever or data['severity']>=7),"emergency":False,"follow_up_questions":["What is your highest temperature, if checked?","Do you have trouble breathing, chest pain, fainting, severe weakness, confusion, or heavy bleeding?"],"safety_note":"Possible causes are not a diagnosis. A clinician can assess you properly."},symptoms)
async def analyze(data):
    if not settings.ai_api_key:return demo_analysis(data)
    result=json.loads(await provider([{"role":"system","content":SYSTEM_PROMPT},{"role":"user","content":json.dumps(data,ensure_ascii=False)}],{"type":"json_object"})); return apply_safety(result,data['symptoms'])
async def chat_reply(message,language,context=''):
    if not settings.ai_api_key:return 'Samajh gaya. Pehle yeh batayein: symptoms kab se hain, severity 1–10 kitni hai, aur kya saans lene mein dikkat, chest pain, behoshi, confusion ya severe bleeding hai?'
    return await provider([{"role":"system","content":"You are MediCare AI, a cautious health triage assistant. Never diagnose with certainty, prescribe medicines, or delay emergency care. Reply briefly in the user's language. Ask focused follow-up questions."},{"role":"user","content":f"Language: {language}\nContext: {context}\nUser: {message}"}])
