import streamlit as st
from PIL import Image
import os
import pickle
st.title("Memory Lane")

# Directory to store contact images and data
CONTACT_DIR = "contacts"
if not os.path.exists(CONTACT_DIR):
    os.makedirs(CONTACT_DIR)

# Load existing contacts from the file
def load_contacts():
    try:
        with open("contacts.pkl", "rb") as f:
            return pickle.load(f)
    except FileNotFoundError:
        return {}

# Save contacts to a file
def save_contacts(contacts):
    with open("contacts.pkl", "wb") as f:
        pickle.dump(contacts, f)

# Function to display contact info
def show_contact_details(contact):
    st.image(contact['image'], width=150)
    st.write(f"**Name**: {contact['name']}")
    st.write(f"**Phone**: {contact['phone']}")
    st.write(f"**Email**: {contact['email']}")
    st.write(f"**Address**: {contact['address']}")
    st.write(f"**Notes**: {contact['notes']}")

# Function to add a new contact
def add_contact(contacts):
    st.header("Add New Contact")

    # Input fields
    name = st.text_input("Name")
    phone = st.text_input("Phone")
    email = st.text_input("Email")
    address = st.text_input("Address")
    notes = st.text_area("Notes")

    # Image uploader
    image = st.file_uploader("Upload Image", type=["jpg", "png", "jpeg"])

    if st.button("Save Contact"):
        if image and name:
            # Save the image to the directory
            image_path = os.path.join(CONTACT_DIR, f"{name}_{phone}.jpg")
            with open(image_path, "wb") as f:
                f.write(image.read())
            
            # Create the contact dictionary
            contact = {
                'name': name,
                'phone': phone,
                'email': email,
                'address': address,
                'notes': notes,
                'image': image_path
            }
            
            # Save the contact to the contacts dictionary
            contacts[name] = contact
            save_contacts(contacts)
            st.success(f"Contact {name} added successfully!")
        else:
            st.error("Name and image are required!")

# Function to display the contact list
def display_contact_list(contacts):
    st.header("Contact List")
    contact_names = list(contacts.keys())
    
    if len(contact_names) == 0:
        st.write("No contacts available.")
    else:
        for name in contact_names:
            if st.button(name):
                show_contact_details(contacts[name])

# Main Streamlit app layout
def main():
    contacts = load_contacts()

    # Sidebar with options
    option = st.sidebar.selectbox("Select an Option", ["View Contacts", "Add Contact"])

    if option == "Add Contact":
        add_contact(contacts)
    elif option == "View Contacts":
        display_contact_list(contacts)

if __name__ == "__main__":
    main()
