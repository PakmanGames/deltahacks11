import streamlit as st
import socketio
import base64
from PIL import Image
import io

# Connect to the Socket.IO server
sio = socketio.Client()

@sio.event
def connect():
    print("Connected to the Socket.IO server")
    sio.emit('register', {'type': 'subscriber'})

sio.connect('http://localhost:5000')

# Streamlit UI setup
st.title("Live Video Feed")
image_placeholder = st.empty()

# Handle incoming frames
@sio.on('frame')
def handle_frame(data):
    # Decode the base64 image
    image_data = base64.b64decode(data)
    image = Image.open(io.BytesIO(image_data))
    
    # Display the image in Streamlit
    image_placeholder.image(image, use_column_width=True)

# Keep Streamlit running
st.write("Connected to the Socket.IO server. Waiting for frames...")