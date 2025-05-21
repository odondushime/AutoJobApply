from pydantic import BaseModel, EmailStr
from typing import Optional

class Settings(BaseModel):
    name: str
    email: EmailStr
    phone: str
    location: str
    resume_path: Optional[str] = None
    cover_letter_path: Optional[str] = None
    linkedin_email: Optional[EmailStr] = None
    linkedin_password: Optional[str] = None

class SettingsUpdate(BaseModel):
    name: Optional[str] = None
    email: Optional[EmailStr] = None
    phone: Optional[str] = None
    location: Optional[str] = None
    resume_path: Optional[str] = None
    cover_letter_path: Optional[str] = None
    linkedin_email: Optional[EmailStr] = None
    linkedin_password: Optional[str] = None 