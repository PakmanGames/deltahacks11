# Facial recognition setup
import streamlit as st
import cv2
import numpy as np

def main():
    st.title("Facial Recognition App")
    FRAME_WINDOW = st.image([])

    while True:
        img_file_buffer = st.camera_input("Capture an image")

        if img_file_buffer is not None:
            # Convert the image to a format for cv2
            bytes_data = img_file_buffer.getvalue()
            np_array = np.frombuffer(bytes_data, np.uint8)
            frame = cv2.imdecode(np_array, cv2.IMREAD_COLOR)

            # make grey
            gray_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

            # Display the processed frame
            FRAME_WINDOW.image(gray_frame, channels="GRAY")
