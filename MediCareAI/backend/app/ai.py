import json, httpx
from .config import settings
from .safety import apply_safety, detect_emergency
SYSTEM_PROMPT='''You are MediCare AI, a cautious health triage assistant for India. You are not a doctor. Never diagnose with certainty, never prescribe prescription medicines, and never advise delaying emergency care. Use simple language matching Hindi, English or Hinglish. Ask for missing critical information. OTC information is general only and must be conservative; never give personalized dosing. Do not include OTC information when key safety information is missing. Return ONLY valid JSON with keys: summary, possible_conditions, risk_level, red_flags, recommended_action, self_care, otc_information, doctor_required, emergency, follow_up_questions, safety_note. risk_level must be Low Risk, Moderate Risk, High Risk or Emergency.'''
def demo_analysis(data):
    symptoms=data['symptoms']; flags=detect_emergency(symptoms)
    if flags:
        return apply_safety({'summary':f'Aapne bataya: {symptoms}','possible_conditions':[],'risk_level':'Emergency','red_flags':flags,'recommended_action':'Seek emergency medical care now.','self_care':[],'otc_information':[],'doctor_required':True,'emergency':True,'follow_up_questions':[],'safety_note':'Emergency warning overrides routine self-care advice.'},symptoms)
    fever=data.get('temperature_c') is not None and data['temperature_c']>=38; sev=data['severity']; risk='High Risk' if sev>=8 else 'Moderate Risk' if fever or sev>=6 else 'Low Risk'
    return apply_safety({'summary':f"Aapne {data['duration']} se {symptoms} bataya hai. Severity {sev}/10 hai.",'possible_conditions':['A common viral illness may be one possibility.','Another infection affecting the reported body area is another possibility.','A non-infectious cause may also explain some symptoms.'],'risk_level':risk,'red_flags':[],'recommended_action':'Monitor symptoms at home and seek professional care if they persist, worsen, or warning signs appear.','self_care':['Rest and drink enough fluids if you can safely do so.','Track temperature and symptom changes.','Avoid medicines that have caused an allergic reaction before.'],'otc_information':[],'doctor_required':risk!='Low Risk','emergency':False,'follow_up_questions':['Symptoms kitne time se hain?','Kya saans lene mein dikkat, chest pain, behoshi, severe bleeding ya confusion hai?'],'safety_note':'Possible causes are not a diagnosis. A qualified clinician can assess you properly.'},symptoms)
async def analyze(data):
    if detect_emergency(data['symptoms']) or not settings.ai_api_key: return demo_analysis(data)
    payload={'model':settings.ai_model,'temperature':0.1,'messages':[{'role':'system','content':SYSTEM_PROMPT},{'role':'user','content':json.dumps(data,ensure_ascii=False)}],'response_format':{'type':'json_object'}}
    headers={'Authorization':f'Bearer {settings.ai_api_key}','Content-Type':'application/json'}
    async with httpx.AsyncClient(timeout=45) as client:
        r=await client.post(f"{settings.ai_api_base_url.rstrip('/')}/chat/completions",headers=headers,json=payload); r.raise_for_status(); result=json.loads(r.json()['choices'][0]['message']['content'])
    return apply_safety(result,data['symptoms'])
