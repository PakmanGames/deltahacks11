import socketio
from aiohttp import web

# create a Socket.IO server
sio = socketio.AsyncServer()

# create a web application
app = web.Application()
sio.attach(app)

# dictionary to store clients
clients = {"publisher": None, "subscriber": None}

@sio.event
async def connect(sid, environ):
    print(f"Client connected: {sid}")

@sio.event
async def disconnect(sid):
    print(f"Client disconnected: {sid}")
    for role, client_sid in clients.items():
        if client_sid == sid:
            clients[role] = None

@sio.event
async def register(sid, data):
    role = data.get("role")
    if role in clients:
        clients[role] = sid
        await sio.emit("registered", {"role": role}, room=sid)
        print(f"Client {sid} registered as {role}")

@sio.event('video_frame')
async def message(sid, data):
    if clients["subscriber"] and sid == clients["publisher"]:
        await sio.emit("frame", data, room=clients["subscriber"])

# run the web application
if __name__ == '__main__':
    web.run_app(app, port=5000)