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