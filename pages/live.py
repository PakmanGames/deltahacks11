import streamlit as st
from streamlit_webrtc import webrtc_streamer, RTCConfiguration
import av
from util.live_prod import main

st.title("Live feed")

# Placeholder for live feed functionality
st.write("This is where the live feed will be displayed.")

main()