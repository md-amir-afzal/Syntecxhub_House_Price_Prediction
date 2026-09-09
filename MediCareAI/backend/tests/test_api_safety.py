from fastapi.testclient import TestClient
from app.main import app
client=TestClient(app)
def test_health():
 r=client.get('/health');assert r.status_code==200;assert r.json()['status']=='ok'
def test_protected_assessment_requires_auth():
 r=client.post('/api/v1/assessments/analyze',json={'patient_name':'A','age':25,'symptoms':'fever','severity':3});assert r.status_code==401
def test_emergency_check():
 r=client.post('/api/v1/safety/emergency-check',params={'symptoms':'severe chest pain and difficulty breathing'});assert r.status_code==200;assert r.json()['emergency'] is True
