import os
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from supabase import create_client, Client
from dotenv import load_dotenv
from schemas import Brand, Drink, DrinkCreate

# load environment variables from .env file
load_dotenv()

# Supabase config
url: str = os.environ.get("SUPABASE_URL")
key: str = os.environ.get("SUPABASE_KEY")

#quick validation
if not url or not key:
    raise ValueError("Missing SUPABASE_URL or SUPABASE_KEY in .env file")

#create supabase client
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

@app.get("/api/drinks", response_model=list[Drink])
def get_drinks():
    drinks_response = supabase.table("drinks").select("*").execute()
    drink_data = drinks_response.data

    brands_response = supabase.table("brands").select("*").execute()
    brand_map = {brand['id']: brand['name'] for brand in brands_response.data}
    results = []

    for drink in drink_data:
        brand_name = brand_map.get(drink['brand_id'], "Unknown Brand")
        #get display name
        display_name = f"{brand_name} {drink['flavour']} {drink['size_ml']}ml"
        #Add computed fields to the dict
        drink['brand_name'] = brand_name
        drink['display_name'] = display_name
        results.append(drink)

    return results

@app.post("/api/drinks", response_model=Drink)
def create_drink(drink: DrinkCreate):
    #convert pydantic model to dict
    data_to_insert = drink.dict()

    #insert to supabase
    response = supabase.table("drinks").insert(data_to_insert).execute()
    
    # Supabase fetches the created record to return
    created_drink = response.data[0]

    # Fetch brand name for the created drink
    brand_response = supabase.table("brands").select("name").eq("id", created_drink["brand_id"]).execute()
    brand_name = brand_response.data["name"]

    created_drink['brand_name'] = brand_name
    created_drink['display_name'] = f"{brand_name} {created_drink['flavour']} {created_drink['size_ml']}ml"

    return created_drink