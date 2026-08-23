from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
import sqlite3
import os

app = FastAPI(title="Real Estate Lead Generator API")

# Enable CORS for the Next.js frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], # In production, restrict this to the Next.js domain
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

DB_NAME = os.path.join(os.path.dirname(__file__), "leads.db")

def get_db_connection():
    if not os.path.exists(DB_NAME):
        return None
    conn = sqlite3.connect(DB_NAME)
    conn.row_factory = sqlite3.Row
    return conn

@app.get("/api/leads")
def get_leads():
    conn = get_db_connection()
    if not conn:
        raise HTTPException(status_code=404, detail="Database not found")
        
    try:
        cursor = conn.cursor()
        cursor.execute("SELECT id, owner_name, property_address, property_value, delinquent_amount, phone_1, email FROM leads ORDER BY id DESC")
        rows = cursor.fetchall()
        
        leads = []
        for row in rows:
            leads.append(dict(row))
            
        return {"leads": leads}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        conn.close()

@app.get("/api/health")
def health_check():
    return {"status": "healthy"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8001)
