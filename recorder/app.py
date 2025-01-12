import numpy as np
import cv2 as cv
import socketio
import base64
import time

sio = socketio.Client()
registered = False

@sio.event
def connect():
    print("Connected to server")
    sio.emit("register", {"type": "publisher"})

@sio.on("registered")
def registered_event(data):
    global registered
    registered = True
    print("Registered as publisher")

sio.connect('http://localhost:5000')
while not registered:
    pass

cap = cv.VideoCapture(0)
if not cap.isOpened():
    print("Cannot open camera")
    exit()
while True:
    # Capture frame-by-frame
    ret, frame = cap.read()
 
    # if frame is read correctly ret is True
    if not ret:
        print("Can't receive frame (stream end?). Exiting ...")
        break
        
    # Encode frame to base64
    _, buffer = cv.imencode('.jpg', frame)
    frame_bytes = base64.b64encode(buffer).decode('utf-8')
    
    # Emit frame
    sio.emit('video_frame', frame_bytes)
    
    # Control frame rate
    # Our operations on the frame come here
    gray = cv.cvtColor(frame, cv.COLOR_BGR2GRAY)
    
    cv.imshow('frame', gray)
    if cv.waitKey(1) == ord('q'):
        break
    
    time.sleep(0.03) # ~30 FPS
 
# When everything done, release the capture
cap.release()
cv.destroyAllWindows()
sio.disconnect()