# Facial recognition setup
import streamlit as st
from streamlit_webrtc import webrtc_streamer
import av
st.title("Live feed")

# Placeholder for live feed functionality
st.write("This is where the live feed will be displayed.")


def video_frame_callback(frame: av.VideoFrame) -> av.VideoFrame:
    img = frame.to_ndarray(format="bgr24")

    flipped = img[::-1,:,:]

    return av.VideoFrame.from_ndarray(flipped, format="bgr24")


webrtc_streamer(key="example", video_frame_callback=video_frame_callback)