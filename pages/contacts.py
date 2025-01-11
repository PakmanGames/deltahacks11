# Lists all contacts, supports add, delete, and view contacts

import streamlit as st
from models import Contact
import os

st.title("Contacts")

contacts: list[Contact] = [
    
]

# Function to display contact info
def show_contact_details(contact: Contact):
    st.image(contact['image'], width=150)
    st.write(f"**Name**: {contact.name}")
    st.write(f"**Phone**: {contact.phone}")
    st.write(f"**Email**: {contact.email}")
    st.write(f"**Date of birth**: {contact.dob}")
    st.write(f"**Main Memory**: {contact.mainMemory}")

# Function to add a new contact
def add_contact(contacts: list[Contact]):
    st.header("Add New Contact")

    # Input fields
    name = st.text_input("Name")
    phone = st.text_input("Phone")
    email = st.text_input("Email")
    dob = st.date_input("Date of birth")
    mainMemory = st.text_area("Main memory")

    # Image uploader
    image = st.file_uploader("Upload Image", type=["jpg", "png", "jpeg"])

    if st.button("Save Contact"):
        if image and name:
            # Save the image to the directory
            image_path = os.path.join("contacts", f"{name}_{phone}.jpg")
            with open(image_path, "wb") as f:
                f.write(image.read())
            
            # Create the contact dictionary
            contact = Contact(
                name=name,
                phone=phone,
                email=email,
                dob=dob,
                mainMemory=mainMemory,
                image=image_path,
                social_handles={}
            )
            
            # Save the contact to the contacts dictionary
            contacts.append(contact)
            
            st.success(f"Contact {name} added successfully!")
        else:
            st.error("Name and image are required!")

# Function to display the contact list
def display_contact_list(contacts: list[Contact]):
    st.header("Contact List")
    
    if len(contacts) == 0:
        st.write("No contacts available.")
    else:
        for contact in contacts:
            if st.button(contact.name):
                show_contact_details(contacts)


# Sidebar with options
option = st.sidebar.selectbox("Select an Option", ["View Contacts", "Add Contact"])

if option == "Add Contact":
    add_contact(contacts)
elif option == "View Contacts":
    display_contact_list(contacts)


