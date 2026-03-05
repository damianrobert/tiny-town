from fastapi import FastAPI
import os
import psycopg2

app = FastAPI()

@app.get("/")
def root():
    return {"message": "TinyTown says hello 👋"}

@app.get("/health")
def health():
    return {"status": "ok"}

@app.get("/db")
def db_check():
    # simple DB connectivity check
    required = ["DB_HOST","DB_NAME","DB_USER","DB_PASSWORD","DB_PORT"]
missing = [k for k in required if not os.getenv(k)]
if missing:
    raise RuntimeError(f"Missing required env vars: {missing}")

conn = psycopg2.connect(
        host=os.getenv("DB_HOST", "db"),
        dbname=os.getenv("DB_NAME", "appdb"),
        user=os.getenv("DB_USER", "appuser"),
        password=os.getenv("DB_PASSWORD"),
        port=int(os.getenv("DB_PORT", "5432")),
    )
    cur = conn.cursor()
    cur.execute("SELECT 1;")
    val = cur.fetchone()[0]
    cur.close()
    conn.close()
    return {"db": "ok", "select_1": val}
