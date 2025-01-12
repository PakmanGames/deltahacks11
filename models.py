from pydantic import BaseModel, Field, model_validator
from pydantic_mongo import AbstractRepository, PydanticObjectId, fields
from datetime import date, datetime
from typing import Optional, List
from pymongo import MongoClient
import app_secrets


class Contact(BaseModel):
    id: Optional[PydanticObjectId] = None
    name: str
    photo: str
    email: str
    phone: str
    dob: datetime
    mainMemory: str
    social_handles: dict[str, str] = {}
    
class ContactsRepository(AbstractRepository[Contact]):
   class Meta:
      collection_name = 'contacts'
    
client = MongoClient(app_secrets.MONGO_URL)
database = client["main"]
contacts_repository = ContactsRepository(database=database)

def get_contact_list() -> list[Contact]:
    return list(contacts_repository.find_by({}))

def delete_contact(contact: Contact):
    contacts_repository.delete(contact)

def save_or_edit_contact(contact: Contact):
    contacts_repository.save(contact)
    