import streamlit as st
from camera_input_live import camera_input_live
import cv2
import face_recognition
import numpy as np
from PIL import Image

from util.images import load_image

image_path_elon = "contacts/elonmusk.jpg"
try:
    elon = load_image(image_path_elon)
except ValueError as e:
    st.error(f"Error loading image: {e}")

def detect_faces(image):
    image_array = np.array(image)
    
    image_bgr = cv2.cvtColor(image_array, cv2.COLOR_RGB2BGR)
    
    # find face locations
    face_locations = face_recognition.face_locations(image_bgr)
    
    # draw rectangle around face
    for (top, right, bottom, left) in face_locations:
        cv2.rectangle(image_array, (left, top), (right, bottom), (0, 255, 0), 2)

    # Return the modified image and number of faces detected
    return image_array, len(face_locations)

# Capture live image using the custom camera_input_live function
image = camera_input_live()

if image:
    # Convert the image to a PIL image for OpenCV processing
    pil_image = Image.open(image)
    
    # Detect faces and get the modified image
    image_with_faces, faces_detected = detect_faces(pil_image)
    
    # Display the modified image with rectangles
    st.image(image_with_faces, caption=f"Faces detected: {faces_detected}")
else:
    st.warning("Please capture an image.")
