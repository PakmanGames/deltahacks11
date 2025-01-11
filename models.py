from pydantic import BaseModel, Field
from datetime import date

class Contact(BaseModel):
    name: str
    photo: str
    email: str
    phone: str
    dob: date
    mainMemory: str
    social_handles: dict[str, str] = {}