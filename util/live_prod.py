import av
from streamlit_webrtc import webrtc_streamer, RTCConfiguration

def main():
    rtc_config = RTCConfiguration({
        "iceServers": [{"urls": "stun:stun.l.google.com:19302"}]
    })


    def video_frame_callback(frame: av.VideoFrame) -> av.VideoFrame:
        img = frame.to_ndarray(format="bgr24")

        flipped = img[::-1,:,:]

        return av.VideoFrame.from_ndarray(flipped, format="bgr24")


    webrtc_streamer(key="example", video_frame_callback=video_frame_callback, rtc_configuration=rtc_config)