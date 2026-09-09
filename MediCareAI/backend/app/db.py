import sqlite3
from pathlib import Path
DB = Path(__file__).resolve().parent.parent / "medicare.db"
def conn():
    c=sqlite3.connect(DB); c.row_factory=sqlite3.Row; return c
def init_db():
    with conn() as c:
        c.execute("CREATE TABLE IF NOT EXISTS users (id INTEGER PRIMARY KEY AUTOINCREMENT, email TEXT UNIQUE NOT NULL, password_hash TEXT NOT NULL, created_at TEXT DEFAULT CURRENT_TIMESTAMP)")
        c.execute("CREATE TABLE IF NOT EXISTS assessments (id INTEGER PRIMARY KEY AUTOINCREMENT, user_id INTEGER NOT NULL, payload TEXT NOT NULL, result TEXT NOT NULL, created_at TEXT DEFAULT CURRENT_TIMESTAMP, FOREIGN KEY(user_id) REFERENCES users(id))")
        c.execute("CREATE INDEX IF NOT EXISTS idx_assessments_user_created ON assessments(user_id, created_at DESC)")
def create_user(email: str, password_hash: str) -> int:
    with conn() as c:
        cur=c.execute("INSERT INTO users(email,password_hash) VALUES(?,?)",(email.lower().strip(),password_hash)); return int(cur.lastrowid)
def get_user(email: str):
    with conn() as c: return c.execute("SELECT * FROM users WHERE email=?",(email.lower().strip(),)).fetchone()
def save_assessment(user_id:int,payload:dict,result:dict):
    import json
    with conn() as c: c.execute("INSERT INTO assessments(user_id,payload,result) VALUES(?,?,?)",(user_id,json.dumps(payload,ensure_ascii=False),json.dumps(result,ensure_ascii=False)))
def get_history(user_id:int,limit:int=30):
    import json
    with conn() as c: rows=c.execute("SELECT id,result,created_at FROM assessments WHERE user_id=? ORDER BY id DESC LIMIT ?",(user_id,limit)).fetchall()
    return [{"id":r["id"],"created_at":r["created_at"],**json.loads(r["result"])} for r in rows]
