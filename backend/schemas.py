from pydantic import BaseModel
from datetime import datetime
from typing import Optional

# Base model with shared attributes
class BrandBase(BaseModel):
    name: str

# Model for reading (includes ID and timestamps)
class Brand(BrandBase):
    id: int
    created_at: datetime

    class Config:
        from_attributes = True

# Model for creating a new drink 
class DrinkBase(BaseModel):
    flavour: str
    size_ml: int

class DrinkCreate(DrinkBase):
    brand_id: int
    caffeine_per_100ml: float # changed as cans usually have caffeine content per 100ml

class Drink(DrinkBase):
    id: int
    brand_id: int
    caffeine_mg: int
    caffeine_per_100ml: float
    brand_name:str
    display_name:str

    class Config:
        from_attributes = True

class ConsumptionBase(BaseModel):
    drink_id: int

class consumptionCreate(ConsumptionBase):
    price_paid: float = 0.0 # default to 0 if not provided

class Consumption(ConsumptionBase):
    id: int
    consumed_at: datetime
    drink_display_name: str
    class Config:
        from_attributes = True 

class AllTimeStats(BaseModel):
    total_ml: int
    total_caffeine: int
    drink_count: int
    total_spent: float

