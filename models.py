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
    
# TODO: Implement the functions to read and write the contacts to a MongoDB database
contents: list[Contact] = []

def get_contact_list() -> list[Contact]:
    return contents

def add_contact(contact: Contact, contacts: list[Contact]):
    contacts.append(contact)