import streamlit as st
import cv2
import face_recognition as frg
import yaml 
import numpy as np
from util.compare_util import recognize
from dataclasses import dataclass

@dataclass
class FaceRecognitionConfig:
    def __init__(self, config_path: str = 'config.yaml'):
        cfg = yaml.load(open(config_path, 'r'), Loader=yaml.FullLoader)
        self.picture_prompt = cfg['INFO']['PICTURE_PROMPT']
        self.webcam_prompt = cfg['INFO']['WEBCAM_PROMPT']

class ImageProcessor:
    @staticmethod
    def process_uploaded_image(image_file):
        bytes_data = image_file.getvalue()
        return cv2.imdecode(np.frombuffer(bytes_data, np.uint8), cv2.IMREAD_COLOR)

class ContactInfoDisplay:
    def __init__(self):
        st.sidebar.title("Contact Information")
        self.name_container = st.sidebar.empty()
        self.memory_container = st.sidebar.empty()
        self.email_container = st.sidebar.empty()
        self.phone_container = st.sidebar.empty()
        self.reset_info()
    
    def reset_info(self):
        self.name_container.info('Name: Unknown')
        
    def update_info(self, name: str, id_val: str, memory: str = None, email: str = None, phone: str = None):
        self.name_container.info(f"Name: {name}")
        if memory:
            self.memory_container.info(f"Main Memory: {memory}")
        if email:
            self.email_container.info(f"Email: {email}")
        if phone:
            self.phone_container.info(f"Phone: {phone}")

class FaceRecognitionApp:
    def __init__(self):
        st.set_page_config(layout="wide")
        self.config = FaceRecognitionConfig()
        self.contact_info = ContactInfoDisplay() # sidebar display
        self.setup_sidebar()
        
    def setup_sidebar(self):
        st.sidebar.title("Settings")
        self.menu = [ "Webcam", "Picture"]
        self.choice = st.sidebar.selectbox("Input type", self.menu)
        self.tolerance = st.sidebar.slider("Tolerance", 0.0, 1.0, 0.5, 0.01)
        st.sidebar.info("Tolerance is the threshold for face recognition. "
                       "The lower the tolerance, the more strict the face recognition. "
                       "The higher the tolerance, the more loose the face recognition.")
    
    def handle_picture_mode(self):
        st.title("Face Recognition App")
        st.write(self.config.picture_prompt)
        uploaded_images = st.file_uploader("Upload", 
                                         type=['jpg','png','jpeg'],
                                         accept_multiple_files=True)
        
        if uploaded_images:
            for image in uploaded_images:
                image = frg.load_image_file(image)
                processed_image, name, id_val = recognize(image, self.tolerance)
                self.contact_info.update_info(name, id_val)
                st.image(processed_image)
        else:
            st.info("Please upload an image")
            
    def _handle_webcam_mode(self):
        img_file_buffer = st.camera_input("Find a Face to Recognize")
        if img_file_buffer is not None and st.button("Submit", key="submit_btn"):
            # Process the uploaded image
            cv2_img = ImageProcessor.process_uploaded_image(img_file_buffer)
            
            # Perform face recognition
            processed_image, name, id_val, mainMemory, email, phone = recognize(cv2_img, self.tolerance)
            
            # Convert the processed image from BGR to RGB for display
            processed_image_rgb = cv2.cvtColor(processed_image, cv2.COLOR_BGR2RGB)
            
            # Display the processed image
            st.image(processed_image_rgb)
            self.contact_info.update_info(name, id_val,mainMemory, email, phone)
                
    def run(self):
        if self.choice == "Picture":
            self.handle_picture_mode()
        else:
            self._handle_webcam_mode()

if __name__ == "__main__":
    app = FaceRecognitionApp()
    app.run()