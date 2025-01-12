import streamlit as st
from camera_input_live import camera_input_live
import cv2
import face_recognition
import numpy as np
from PIL import Image

from util.images import load_image

# Load the reference image (Elon Musk) and encode the face
image_path_elon = "contacts/elonmusk.jpg"
try:
    elon_image = cv2.imread(image_path_elon)
    if elon_image is None:
        st.error("Failed to load the reference image.")
        st.stop()
except ValueError as e:
    st.error(f"Error loading image: {e}")
    st.stop()

# Convert to RGB (OpenCV loads images in BGR by default)
elon_image_rgb = cv2.cvtColor(elon_image, cv2.COLOR_BGR2RGB)

# Encode Elon Musk's face and ensure it's valid
elon_face_encodings = face_recognition.face_encodings(elon_image_rgb)
if not elon_face_encodings:
    st.error("No face detected in the reference image.")
    st.stop()
elon_face_encoding = elon_face_encodings[0]

def detect_and_compare_faces(live_image, reference_encoding):
    # Convert the PIL image to a numpy array
    image_array = np.array(live_image)
    
    # Convert the image from RGB to BGR (for OpenCV)
    image_bgr = cv2.cvtColor(image_array, cv2.COLOR_RGB2BGR)
    
    # Detect face locations and encodings
    face_locations = face_recognition.face_locations(image_bgr)
    face_encodings = face_recognition.face_encodings(image_bgr, face_locations)

    if not face_encodings:
        st.error("No face detected in the live image.")
        return image_array, 0

    # Compare faces
    face_match = face_recognition.compare_faces([reference_encoding], face_encodings[0])
    if face_match:
        st.success("Face Match Found!")
    else:
        st.error("Face Match Not Found!")
    
    # Draw rectangles around detected faces
    for (top, right, bottom, left) in face_locations:
        cv2.rectangle(image_array, (left, top), (right, bottom), (0, 255, 0), 2)

    return image_array, len(face_locations)

# Capture live image using the custom camera_input_live function
image = camera_input_live()

if image:
    # Convert the live image to a PIL image for processing
    pil_image = Image.open(image)
    
    # Compare the live feed with the reference image
    # THE ISSUE IS HERE
    image_with_faces, faces_detected = detect_and_compare_faces(pil_image, elon_face_encoding)
    
    # Display the modified image with rectangles
    # THE ISSUE IS HERE
    st.image(image_with_faces, caption=f"Faces detected: {faces_detected}")
    # st.image(elon_image_rgb)
else:
    st.warning("Please capture an image.")
