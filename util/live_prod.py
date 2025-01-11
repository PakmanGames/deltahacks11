import av
from streamlit_webrtc import webrtc_streamer, RTCConfiguration
from twilio.rest import Client
from app_secrets import TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN

client = Client(TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN)
token = client.tokens.create()

def main():
    rtc_config = RTCConfiguration({
        "iceServers": token.ice_servers
    })


    webrtc_streamer(key="example", rtc_configuration=rtc_config, media_stream_constraints={
        "video": True,
        "audio": False
    })
