import os
import json
from fastapi import FastAPI, HTTPException, Header, Depends, Request
from fastapi.middleware.cors import CORSMiddleware
from slowapi import Limiter
from slowapi.util import get_remote_address
from slowapi.errors import RateLimitExceeded
from slowapi.middleware import SlowAPIMiddleware
from starlette.responses import JSONResponse
from supabase import create_client, Client
from dotenv import load_dotenv
from datetime import date as date_type, timedelta
import google.generativeai as genai
from schemas import Brand, Drink, DrinkCreate, consumptionCreate, Consumption, AllTimeStats, ChatRequest, ChatResponse

# Security Dependency
def verify_admin(x_admin_key: str = Header(default=None)):
    secret = os.environ.get("ADMIN_SECRET")

    # If no secret is set on the server, we might want to fail safe
    if not secret:
        raise HTTPException(status_code=500, detail="Server misconfigured: No Admin Secret")

    if x_admin_key != secret:
        raise HTTPException(status_code=401, detail="Unauthorized: Wrong Admin Key")

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

# Gemini config
gemini_key = os.environ.get("GEMINI_API_KEY")
if gemini_key:
    genai.configure(api_key=gemini_key)

limiter = Limiter(key_func=get_remote_address)

app = FastAPI()

app.state.limiter = limiter

@app.exception_handler(RateLimitExceeded)
async def rate_limit_handler(request: Request, exc: RateLimitExceeded):
    return JSONResponse(status_code=429, content={"detail": "Too many requests. Slow down."})

app.add_middleware(SlowAPIMiddleware)
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

@app.post("/api/drinks", response_model=Drink, dependencies=[Depends(verify_admin)])
def create_drink(drink: DrinkCreate):
    #calc total caffeine content
    total_caffeine_mg = int((drink.caffeine_per_100ml * drink.size_ml) / 100)
    #convert pydantic model to dict
    data_to_insert = {
        "brand_id": drink.brand_id, 
        "flavour": drink.flavour, 
        "size_ml": drink.size_ml,
        "caffeine_mg": total_caffeine_mg
    }
    

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

@app.post("/api/brands", response_model=Brand, dependencies=[Depends(verify_admin)])
def create_brand(brand: Brand):
    #convert pydantic model to dict
    data_to_insert = brand.dict()

    #insert to supabase
    response = supabase.table("brands").insert(data_to_insert).execute()
    
    # Supabase fetches the created record to return
    created_brand = response.data[0]
    return created_brand 

@app.post("/api/consumptions", response_model=Consumption, dependencies=[Depends(verify_admin)])
def log_consumption(consumption: consumptionCreate):
    #convert pydantic model to dict
    data_to_insert = consumption.dict()

    result = supabase.table("consumptions").insert(data_to_insert).execute()
    new_consumption = result.data[0]

    drink_res = supabase.table("drinks").select("*, brands(name)").eq("id", new_consumption["drink_id"]).single().execute()
    drink_data = drink_res.data

    brand_name = drink_data["brands"]["name"]
    display_name = f"{brand_name} {drink_data['flavour']} {drink_data['size_ml']}ml"

    new_consumption['drink_display_name'] = display_name

    return new_consumption

@app.get("/api/consumptions/top_10", response_model=list[Consumption])
def get_consumptions_limited():
    limit = 10
    result = supabase.table("consumptions").select("*, drinks(*, brands(name))").order("consumed_at", desc=True).limit(limit).execute()

    results = []
    for record in result.data:
        drink = record["drinks"]
        brand_name = drink["brands"]

        display_name = f"{brand_name['name']} {drink['flavour']} {drink['size_ml']}ml"
        record["drink_display_name"] = display_name

        results.append(record)

    return results

@app.get("/api/consumptions", response_model=list[Consumption])
def get_consumptions():
    result = supabase.table("consumptions").select("*, drinks(*, brands(name))").order("consumed_at", desc=True).execute()

    results = []
    for record in result.data:
        drink = record["drinks"]
        brand_name = drink["brands"]

        display_name = f"{brand_name['name']} {drink['flavour']} {drink['size_ml']}ml"
        record["drink_display_name"] = display_name

        results.append(record)

    return results

@app.get("/api/stats", response_model=AllTimeStats)
def get_all_time_stats():
    response = supabase.table("consumptions").select("price_paid, drinks(size_ml, caffeine_mg)").execute()

    total_vol = 0
    total_mg = 0
    total_money = 0
    drink_count = 0

    for record in response.data:
        drink = record["drinks"]
        total_vol += drink["size_ml"]
        total_mg += drink["caffeine_mg"]

        if record["price_paid"]:
            total_money += record["price_paid"]

        drink_count += 1

    return{
        "total_ml": total_vol,
        "total_caffeine": total_mg,
        "drink_count": drink_count,
        "total_spent": total_money
    }

@app.get("/api/stats/daily")
def get_daily_caffeine_stats(date: date_type):
    start_date = date
    end_date = date + timedelta(days=1)

    response = supabase.table("consumptions") \
        .select("drinks(caffeine_mg)") \
        .gte("consumed_at", str(start_date)) \
        .lt("consumed_at", str(end_date)) \
        .execute()

    total_mg = 0
    for record in response.data:
        drink = record.get("drinks")
        if drink and drink.get("caffeine_mg"):
            total_mg += drink["caffeine_mg"]

    return total_mg

@app.get("/api/charts/stacked")
def get_stacked_chart(group_by: str = "brand"):
    # 1. Fetch data including BOTH flavour and brand name
    response = supabase.table("consumptions") \
        .select("consumed_at, price_paid, drinks(flavour, brands(name))") \
        .order("consumed_at") \
        .execute()
    
    # 2. Pivot Data
    grouped = {}
    all_keys = set()

    for record in response.data:
        date_str = record['consumed_at'].split('T')[0]
        
        # DYNAMIC KEY SELECTION
        if group_by == "flavour":
            key_name = record['drinks']['flavour']
        else:
            key_name = record['drinks']['brands']['name']
            
        all_keys.add(key_name)
        
        price = record['price_paid'] or 0.0
        
        if date_str not in grouped:
            grouped[date_str] = {}
        
        current_total = grouped[date_str].get(key_name, 0.0)
        grouped[date_str][key_name] = current_total + price

    # 3. Format for Frontend
    results = []
    for date, values in grouped.items():
        row = {"date": date}
        for k in all_keys:
            row[k] = values.get(k, 0.0)
        results.append(row)
        
    return results

@app.get("/api/charts/brand-distribution")
def get_brand_distribution(group_by: str = "brand"):
    # Fetch drinks and brands to handle both cases
    response = supabase.table("consumptions").select("drinks(flavour, brands(name))").execute()

    counts = {}
    for record in response.data:
        drink = record.get("drinks")
        if not drink: 
            continue
            
        # DYNAMIC KEY SELECTION
        if group_by == "flavour":
            key = drink.get("flavour", "Unknown")
        else:
            # Safely get brand name
            brand = drink.get("brands")
            key = brand.get("name", "Unknown") if brand else "Unknown"
            
        counts[key] = counts.get(key, 0) + 1
    
    if not counts:
        return {"labels": [], "data": []}
    
    labels = list(counts.keys())
    data = list(counts.values())

    return {"labels": labels, "data": data}

SYSTEM_PROMPT = """You are an analyst for a personal energy drink tracker app.
You will be given a JSON array of the user's drink consumption history and a question about it.
Answer the question using only the data provided.

You MUST respond with valid JSON only — no markdown, no extra text.

If the answer is best expressed as text, respond with:
{"type": "text", "answer": "your answer here"}

If the answer is best expressed as a chart, respond with:
{"type": "chart", "chart_type": "bar", "title": "chart title", "labels": ["label1", "label2"], "data": [10, 20]}

Use "bar" for comparisons (days of week, brands, etc.) and "pie" for distributions.
Keep answers concise and friendly."""

@app.post("/api/chat", response_model=ChatResponse)
@limiter.limit("5/minute;20/hour")
def chat(request: ChatRequest, req: Request):
    if not gemini_key:
        raise HTTPException(status_code=500, detail="GEMINI_API_KEY not configured")

    # Fetch all consumptions with drink and brand info
    result = supabase.table("consumptions") \
        .select("consumed_at, price_paid, drinks(flavour, caffeine_mg, size_ml, brands(name))") \
        .order("consumed_at") \
        .execute()

    # Build a compact context array for the model
    context = []
    days = ["Monday","Tuesday","Wednesday","Thursday","Friday","Saturday","Sunday"]
    for record in result.data:
        drink = record.get("drinks") or {}
        brand = (drink.get("brands") or {}).get("name", "Unknown")
        dt = record["consumed_at"].split("T")[0]
        dow = days[date_type.fromisoformat(dt).weekday()]
        context.append({
            "date": dt,
            "day_of_week": dow,
            "drink": f"{brand} {drink.get('flavour','')}".strip(),
            "size_ml": drink.get("size_ml"),
            "caffeine_mg": drink.get("caffeine_mg"),
            "price_paid": record.get("price_paid") or 0.0
        })

    prompt = f"""Consumption data (JSON):
{json.dumps(context, indent=2)}

User question: {request.question}"""

    model = genai.GenerativeModel(
        model_name="gemini-3-flash-preview",
        generation_config={"response_mime_type": "application/json"}
    )
    response = model.generate_content([SYSTEM_PROMPT, prompt])

    try:
        parsed = json.loads(response.text)
    except Exception:
        parsed = {"type": "text", "answer": response.text}

    return parsed