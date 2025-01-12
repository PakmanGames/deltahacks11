# Facial recognition setup
import streamlit as st
import cv2
import numpy as np
import face_recognition
from streamlit_webrtc import webrtc_streamer, RTCConfiguration

def main():
    st.title("Facial Recognition App")
    FRAME_WINDOW = st.image([])

    image_path = 'contacts/Elon Musk.jpg'
    reference_image = cv2.imread(image_path)
    if reference_image is not None:
        # logic to compare with face_recognition
        reference_image_rgb = cv2.cvtColor(reference_image, cv2.COLOR_BGR2RGB)
        reference_encoding = face_recognition.face_encodings(reference_image_rgb)[0]
        if reference_encodings:
            reference_encoding = reference_encodings[0]
        else:
            st.error("No face found in the reference image.")
            return

    # img_file_buffer = st.camera_input("Capture an image")
    webrtc_streamer(key="sample")
    if img_file_buffer is not None:
        # Convert the image to a format for cv2
        bytes_data = img_file_buffer.getvalue()
        np_array = np.frombuffer(bytes_data, np.uint8)
        frame = cv2.imdecode(np_array, cv2.IMREAD_COLOR)

        # make grey
        # gray_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        frame_encodings = face_recognition.face_encodings(frame_rgb)

        if frame_encodings:
            frame_encoding = frame_encodings[0]
            # Compare the captured image with the reference image
            results = face_recognition.compare_faces([reference_encoding], frame_encoding)
            if results[0]:
                st.success("Face matched!")
            else:
                st.error("Face not matched!")
        else:
            st.error("No face found in the captured image.")

        # Display the processed frame
        FRAME_WINDOW.image(gray_frame, channels="GRAY")
