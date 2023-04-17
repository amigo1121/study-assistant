import socketio
import logging
from app.api.api_v1.endpoints.security import get_current_user

logging.basicConfig(
    filename="example.log",
    level=logging.DEBUG,
    format="%(asctime)s %(levelname)s: %(message)s",
)

sio_server = socketio.AsyncServer(async_mode="asgi", cors_allowed_origins=[])
sio_app = socketio.ASGIApp(socketio_server=sio_server, socketio_path="socket")


@sio_server.on("connect")
async def handle_connect(sid, environ, auth):
    logging.info(f"{sid}:  connected")
    logging.error(f'token: {auth.get("token")}')
    try:
        user = get_current_user(token=auth.get("token"))
        username = user.username
        sio_server.enter_room(sid, username)
        logging.info(f"Client {sid} connect and joined room {username}")
    except Exception as e:
        logging.error(e)


@sio_server.on("disconnect")
async def handle_disconnect(sid):
    rooms = sio_server.rooms(sid)
    for room in rooms:
        sio_server.leave_room(sid, room)
        logging.info(f"Remove client {sid} from room {room}")


@sio_server.on("send_message")
async def handle_message(sid, data):
    message = data.get("message")
    logging.info(message)
    try:
        await sio_server.emit(
            "new_message", data={"message": "Hello, client"}, room=sid
        )
    except Exception as e:
        logging.error(f"Error emitting new_message event: {e}")
