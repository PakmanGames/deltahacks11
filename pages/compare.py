import streamlit as st
import cv2
import face_recognition as frg
import yaml 
from util.compare_util import recognize, build_dataset
from dataclasses import dataclass

@dataclass
class FaceRecognitionConfig:
    def __init__(self, config_path: str = 'config.yaml'):
        cfg = yaml.load(open(config_path, 'r'), Loader=yaml.FullLoader)
        self.picture_prompt = cfg['INFO']['PICTURE_PROMPT']
        self.webcam_prompt = cfg['INFO']['WEBCAM_PROMPT']

class StudentInfoDisplay:
    def __init__(self):
        st.sidebar.title("Student Information")
        self.name_container = st.sidebar.empty()
        self.id_container = st.sidebar.empty()
        self.reset_info()
    
    def reset_info(self):
        self.name_container.info('Name: Unknown')
        self.id_container.success('ID: Unknown')
        
    def update_info(self, name: str, id_val: str):
        self.name_container.info(f"Name: {name}")
        self.id_container.success(f"ID: {id_val}")

class FaceRecognitionApp:
    def __init__(self):
        st.set_page_config(layout="wide")
        self.config = FaceRecognitionConfig()
        # self.student_info = StudentInfoDisplay() # sidebar display
        self.setup_sidebar()
        
    def setup_sidebar(self):
        st.sidebar.title("Settings")
        self.menu = ["Picture", "Webcam"]
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
                self.student_info.update_info(name, id_val)
                st.image(processed_image)
        else:
            st.info("Please upload an image")
            
    def handle_webcam_mode(self):
        st.title("Face Recognition App")
        st.write(self.config.webcam_prompt)
        frame_window = st.image([])
        
        cam = cv2.VideoCapture(0)
        cam.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
        cam.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)
        
        while True:
            ret, frame = cam.read()
            if not ret:
                st.error("Failed to capture frame from camera")
                st.info("Please turn off the other app that is using the camera and restart app")
                st.stop()
                
            processed_frame, name, id_val = recognize(frame, self.tolerance)
            processed_frame = cv2.cvtColor(processed_frame, cv2.COLOR_BGR2RGB)
            self.student_info.update_info(name, id_val)
            frame_window.image(processed_frame)
            
    def setup_developer_section(self):
        with st.sidebar.form(key='my_form'):
            st.title("Developer Section")
            if st.form_submit_button(label='REBUILD DATASET'):
                with st.spinner("Rebuilding dataset..."):
                    build_dataset()
                st.success("Dataset has been reset")
                
    def run(self):
        if self.choice == "Picture":
            self.handle_picture_mode()
        else:
            self.handle_webcam_mode()
        self.setup_developer_section()

if __name__ == "__main__":
    app = FaceRecognitionApp()
    app.run()