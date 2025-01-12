import streamlit as st 
import cv2
import numpy as np
from util.compare_util import face_manager

class ImageProcessor:
    @staticmethod
    def process_uploaded_image(image_file):
        bytes_data = image_file.getvalue()
        return cv2.imdecode(np.frombuffer(bytes_data, np.uint8), cv2.IMREAD_COLOR)

class UploadApp:
    def __init__(self):
        st.set_page_config(layout="wide")
        st.title("MemoryLane contact upload")
        st.write("Upload contacts that you want to remember.")
        self.menu = ["Adding", "Deleting", "Adjusting"]
        self.choice = st.sidebar.selectbox("Options", self.menu)
        
    def handle_adding(self):
        name = st.text_input("Name", placeholder='Enter name')
        id_val = st.text_input("ID", placeholder='Enter id')
        upload = st.radio("Upload image or use webcam", ("Upload", "Webcam"))
        
        if upload == "Upload":
            self._handle_upload_image(name, id_val)
        else:
            self._handle_webcam_image(name, id_val)
    
    def _handle_upload_image(self, name, id_val):
        uploaded_image = st.file_uploader("Upload", type=['jpg','png','jpeg'])
        if uploaded_image is not None:
            st.image(uploaded_image)
            if st.button("Submit", key="submit_btn"):
                self._process_submission(name, id_val, uploaded_image)
    
    def _handle_webcam_image(self, name, id_val):
        img_file_buffer = st.camera_input("Take a picture")
        if img_file_buffer is not None and st.button("Submit", key="submit_btn"):
            cv2_img = ImageProcessor.process_uploaded_image(img_file_buffer)
            self._process_submission(name, id_val, cv2_img)
    
    def _process_submission(self, name, id_val, image):
        if name == "" or id_val == "":
            st.error("Please enter name and ID")
            return
            
        # Convert UploadedFile to cv2 image if needed
        if hasattr(image, 'read'):
            image = ImageProcessor.process_uploaded_image(image)
            
        ret = face_manager.submit_new(name, id_val, image)
        if ret == 1:
            st.success("Contact Added")
        elif ret == 0:
            st.error("Contact ID already exists")
        elif ret == -1:
            st.error("There is no face in the picture")
    
    def handle_deleting(self):
        id_val = st.text_input("ID", placeholder='Enter id')
        if st.button("Submit", key="submit_btn"):
            name, image, _ = face_manager.get_info(id_val)
            if name is None and image is None:
                st.error("Contact ID does not exist")
            else:
                st.success(f"Name of contact with ID {id_val} is: {name}")
                st.warning("Please check the image below to make sure you are deleting the right contact")
                st.image(image)
                if st.button("Delete", key="del_btn"):
                    if face_manager.delete_one(id_val):
                        st.success("Contact deleted")
                        print("success delete")
                    else:
                        st.error("Contact deletion failed")
                        print("failed delete")
    
    def handle_adjusting(self):
        # Placeholder for adjusting functionality
        st.write("Adjusting functionality coming soon")
    
    def run(self):
        if self.choice == "Adding":
            self.handle_adding()
        elif self.choice == "Deleting":
            self.handle_deleting()
        elif self.choice == "Adjusting":
            self.handle_adjusting()

if __name__ == "__main__":
    app = UploadApp()
    app.run()