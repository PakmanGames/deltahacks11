import streamlit as st
from streamlit_webrtc import webrtc_streamer, RTCConfiguration
import av

st.title('Live Video Feed with Streamlit WebRTC')

# RTC_CONFIGURATION = RTCConfiguration(
#     {
#         'iceServers': [{'urls': ['stun:stun.l.google.com:19302']}]
#     }
# )

RTC_CONFIGURATION = RTCConfiguration(
    {
        'iceServers': [
            {'urls': ['stun:stun.l.google.com:19302']},  # Public STUN server
            {
                'urls': ['turn:openrelay.metered.ca:80'],  # Public TURN server (for testing)
                'username': 'openrelayproject',
                'credential': 'openrelayproject'
            }
        ]
    }
)

# Define a video frame callback to display the live feed
def video_frame_callback(frame):
    img = frame.to_ndarray(format='bgr24')  # Convert frame to a NumPy array (OpenCV format)
    return av.VideoFrame.from_ndarray(img, format='bgr24')

# Initialize the WebRTC streamer with the callback
# webrtc_streamer(key='example', video_frame_callback=video_frame_callback)
webrtc_streamer(key='example', rtc_configuration=RTC_CONFIGURATION, video_frame_callback=video_frame_callback)

