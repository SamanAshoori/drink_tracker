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
    caffeine_mg: int

class DrinkCreate(DrinkBase):
    brand_id: int

class Drink(DrinkBase):
    id: int
    brand_id: int
    caffeine_per_100ml: float
    brand_name:str
    display_name:str

    class Config:
        from_attributes = True