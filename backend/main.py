import os
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from supabase import create_client, Client
from dotenv import load_dotenv
from schemas import Brand

# 1. Load env vars
load_dotenv()

url: str = os.environ.get("SUPABASE_URL")
key: str = os.environ.get("SUPABASE_KEY")

# 2. Check if keys exist (Early fail if config is wrong)
if not url or not key:
    raise ValueError("Missing SUPABASE_URL or SUPABASE_KEY in .env file")

# 3. Initialize Supabase
supabase: Client = create_client(url, key)

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def read_root():
    return {"status": "ok", "message": "API connected to Supabase"}

# 4. Real Database Endpoint
@app.get("/api/brands", response_model=list[Brand])
def get_brands():
    # Query the 'brands' table, select all columns
    response = supabase.table("brands").select("*").execute()
    
    # Supabase returns data in response.data
    return response.data