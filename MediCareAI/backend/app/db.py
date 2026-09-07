import json,sqlite3
from datetime import datetime,timezone
from pathlib import Path
DB=Path(__file__).resolve().parent.parent/'medicare.db'
def _connect():
 c=sqlite3.connect(DB); c.row_factory=sqlite3.Row; return c
def init_db():
 with _connect() as c:
  c.execute('CREATE TABLE IF NOT EXISTS users (id INTEGER PRIMARY KEY,email TEXT UNIQUE NOT NULL,password_hash TEXT NOT NULL,created_at TEXT NOT NULL)')
  c.execute('CREATE TABLE IF NOT EXISTS assessments (id INTEGER PRIMARY KEY,user_id INTEGER,created_at TEXT NOT NULL,data_json TEXT NOT NULL,result_json TEXT NOT NULL)')
  c.execute('CREATE INDEX IF NOT EXISTS idx_assessments_user ON assessments(user_id,created_at DESC)')
def create_user(email,password_hash):
 with _connect() as c: return int(c.execute('INSERT INTO users(email,password_hash,created_at) VALUES(?,?,?)',(email.lower().strip(),password_hash,datetime.now(timezone.utc).isoformat())).lastrowid)
def get_user(email):
 with _connect() as c: return c.execute('SELECT * FROM users WHERE email=?',(email.lower().strip(),)).fetchone()
def save_assessment(user_id,data,result):
 with _connect() as c: return c.execute('INSERT INTO assessments(user_id,created_at,data_json,result_json) VALUES(?,?,?,?)',(user_id,datetime.now(timezone.utc).isoformat(),json.dumps(data,ensure_ascii=False),json.dumps(result,ensure_ascii=False))).lastrowid
def list_assessments(user_id=0,limit=30):
 with _connect() as c: rows=c.execute('SELECT id,created_at,result_json FROM assessments WHERE user_id=? ORDER BY created_at DESC LIMIT ?',(user_id,limit)).fetchall()
 return [{'id':r['id'],'created_at':r['created_at'],'result':json.loads(r['result_json'])} for r in rows]
