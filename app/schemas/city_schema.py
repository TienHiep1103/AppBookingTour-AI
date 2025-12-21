from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime


class CityBase(BaseModel):
    """Base schema for City"""
    name: str = Field(..., max_length=255, description="City name")
    code: Optional[str] = Field(None, max_length=50, description="City code")
    region: Optional[str] = Field(None, description="Region (North, Central, South)")
    is_popular: bool = Field(default=False, description="Whether the city is popular")
    slug: str = Field(..., max_length=255, description="URL-friendly slug")
    description: Optional[str] = Field(None, description="City description")
    image_url: Optional[str] = Field(None, max_length=500, description="City image URL")
    is_active: bool = Field(default=True, description="Whether the city is active")


class CityCreate(CityBase):
    """Schema for creating a new City"""
    pass


class CityUpdate(BaseModel):
    """Schema for updating an existing City"""
    name: Optional[str] = Field(None, max_length=255)
    code: Optional[str] = Field(None, max_length=50)
    region: Optional[str] = None
    is_popular: Optional[bool] = None
    slug: Optional[str] = Field(None, max_length=255)
    description: Optional[str] = None
    image_url: Optional[str] = Field(None, max_length=500)
    is_active: Optional[bool] = None


class CityResponse(CityBase):
    """Schema for City response"""
    id: int
    created_at: datetime
    updated_at: Optional[datetime]

    class Config:
        from_attributes = True  # SQLAlchemy ➜ Pydantic


class CitySimple(BaseModel):
    """Simplified City schema for nested responses"""
    id: int
    name: str
    code: Optional[str]
    slug: str
    is_popular: bool
    image_url: Optional[str]

    class Config:
        from_attributes = True
