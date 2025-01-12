# Lists all contacts, supports add, delete, and view contacts

import streamlit as st
from models import Contact, get_contact_list, save_or_edit_contact
import os
import numpy as np
import cv2

st.title("Contacts")

contacts = get_contact_list()

# Function to display contact info
def show_contact_details(contact: Contact):
    st.image(contact.photo, width=150)
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
    dob = st.date_input("Date of Birth")
    mainMemory = st.text_area("Main Memory")

    # Image input choice
    st.subheader("Add a Photo")
    input_choice = st.radio("Choose how to add a photo:", ["Upload Image", "Take Picture with Webcam"])

    image = None
    if input_choice == "Upload Image":
        # File uploader for image
        image = st.file_uploader("Upload Image", type=["jpg", "png", "jpeg"])
    elif input_choice == "Take Picture with Webcam":
        # Webcam input for image
        img_file_buffer = st.camera_input("Take a Picture")
        if img_file_buffer:
            # Convert the webcam image to a format that can be saved
            image = img_file_buffer

    if st.button("Save Contact"):
        if image and name:
            # Determine the image path
            image_path = os.path.join("contacts", f"{name}_{phone}.jpg")

            # Handle the image saving for both file uploader and webcam input
            if input_choice == "Upload Image":
                with open(image_path, "wb") as f:
                    f.write(image.read())
            elif input_choice == "Take Picture with Webcam":
                # Convert webcam image to OpenCV format and save
                img_array = np.frombuffer(image.getvalue(), np.uint8)
                cv2_img = cv2.imdecode(img_array, cv2.IMREAD_COLOR)
                cv2.imwrite(image_path, cv2_img)

            # Create the contact dictionary
            contact = Contact(
                name=name,
                phone=phone,
                email=email,
                dob=dob,
                mainMemory=mainMemory,
                photo=image_path,
                social_handles={}
            )

            # Save the contact to the contacts list
            save_or_edit_contact(contact)

            st.success(f"Contact {name} added successfully!")
        else:
            st.error("Name and photo are required!")

# Function to display the contact list
def display_contact_list(contacts: list[Contact]):
    st.header("Contact List")
    
    if len(contacts) == 0:
        st.write("No contacts available.")
    else:
        for contact in contacts:
            if st.button(contact.name):
                show_contact_details(contact)


# Sidebar with options
option = st.sidebar.selectbox("Select an Option", ["View Contacts", "Add Contact"])

if option == "Add Contact":
    add_contact(contacts)
elif option == "View Contacts":
    display_contact_list(contacts)


