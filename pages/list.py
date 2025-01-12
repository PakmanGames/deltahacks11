import streamlit as st
import numpy as np
from dataclasses import dataclass
from typing import List, Optional
from util.compare_util import get_all_info

@dataclass
class Contact:
    name: str
    image: np.ndarray  # Now np.ndarray is defined
    id: str

def fetch_contacts() -> List[Contact]:
    contacts_data = get_all_info()
    return [Contact(name=name, image=image, id=id_val) 
            for name, image, id_val in contacts_data]

def show_contact_details(contact: Contact):
    st.subheader(f"Contact Details - {contact.name}")
    col1, col2 = st.columns(2)
    with col1:
        st.image(contact.image, caption=contact.name)
    with col2:
        st.write(f"ID: {contact.id}")
        st.write(f"Name: {contact.name}")

def display_contact_list():
    st.title("Contact List")
    contacts = fetch_contacts()
    
    if not contacts:
        st.write("No contacts available.")
        return
        
    # Display contacts in a vertical list
    for idx, contact in enumerate(contacts):
        with st.container():
            col1, col2 = st.columns([1, 2])
            with col1:
                st.image(contact.image, width=150)
            with col2:
                st.subheader(contact.name)
                st.write(f"ID: {contact.id}")
                if st.button("View Details", key=f"contact_{idx}"):
                    show_contact_details(contact)
            st.divider()  # Add visual separation between contacts

if __name__ == "__main__":
    display_contact_list()