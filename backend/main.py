import os
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from supabase import create_client, Client
from dotenv import load_dotenv
from schemas import Brand, Drink, DrinkCreate, consumptionCreate, Consumption, AllTimeStats

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

@app.post("/api/brands", response_model=Brand)
def create_brand(brand: Brand):
    #convert pydantic model to dict
    data_to_insert = brand.dict()

    #insert to supabase
    response = supabase.table("brands").insert(data_to_insert).execute()
    
    # Supabase fetches the created record to return
    created_brand = response.data[0]
    return created_brand 

@app.post("/api/consumptions", response_model=Consumption)
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

@app.get("/api/consumptions", response_model=list[Consumption])
def get_consumptions():
    result = supabase.table("consumptions").select("*, drinks(*, brands(name))").order("consumed_at", desc=True).limit(10).execute()

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

@app.get("/api/charts/stacked")
def get_stacked_chart():
    # 1. Fetch all consumptions with drink names and prices
    response = supabase.table("consumptions") \
        .select("consumed_at, price_paid, drinks(flavour, brands(name))") \
        .order("consumed_at") \
        .execute()
    
    # 2. Pivot Data in Python
    # We want: { "2023-10-27": { "Red Bull": 1.50, "Monster": 0.00 } }
    grouped = {}
    all_drink_names = set()

    for record in response.data:
        # Get Date string (YYYY-MM-DD)
        date_str = record['consumed_at'].split('T')[0]
        
        # Create a combined name "Brand Flavour"
        b_name = record['drinks']['brands']['name']
        f_name = record['drinks']['flavour']
        drink_name = f"{b_name} {f_name}"
        all_drink_names.add(drink_name)
        
        # Get price (handle nulls)
        price = record['price_paid'] or 0.0
        
        # Initialize dictionary for this date
        if date_str not in grouped:
            grouped[date_str] = {}
        
        # Add price to existing total
        current_total = grouped[date_str].get(drink_name, 0.0)
        grouped[date_str][drink_name] = current_total + price

    # 3. Format for Frontend
    # Create a list where every date has a key for EVERY drink (filling 0.0 if missing)
    results = []
    for date, values in grouped.items():
        row = {"date": date}
        for name in all_drink_names:
            row[name] = values.get(name, 0.0)
        results.append(row)
        
    return results