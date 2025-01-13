# from flask import Flask, render_template, request
# from flask_socketio import SocketIO, join_room
# import json
# import uuid

# # Create Flask app instance
# app = Flask(__name__)
# socketio = SocketIO(app)

# @app.route("/", methods=['GET'])
# def index():
#     return render_template('consumer.html')

# def send_message(event, namespace, room, message):
#     socketio.emit(event, message, namespace=namespace, room=room)

# # Initialize parameters before each request (Flask 3.x no longer supports before_first_request)
# @app.before_request
# def initialize_params():
#     if not hasattr(app.config, 'uid'):
#         sid = str(uuid.uuid4())
#         app.config['uid'] = sid
#         print("initialize_params - Session ID stored =", sid)

# @app.route('/consumetasks', methods=['POST'])
# def consumetasks():
#     if request.method == 'POST':
#         data = request.json
#         if data:
#             print("Received Data = ", data)
#             roomid = app.config['uid']
#             var = json.dumps(data)
#             send_message(event='msg', namespace='/collectHooks', room=roomid, message=var)
#     return 'OK'

# @socketio.on('connect', namespace='/collectHooks')
# def socket_connect():
#     print('Client Connected To NameSpace /collectHooks - ', request.sid)

# @socketio.on('disconnect', namespace='/collectHooks')
# def socket_disconnect():
#     print('Client disconnected From NameSpace /collectHooks - ', request.sid)

# @socketio.on('join_room', namespace='/collectHooks')
# def on_room():
#     if app.config['uid']:
#         room = str(app.config['uid'])
#         print(f"Socket joining room {room}")
#         join_room(room)

# @socketio.on_error_default
# def error_handler(e):
#     print(f"socket error: {e}, {str(request.event)}")

# if __name__ == "__main__":
#     socketio.run(app, host='localhost', port=5001, debug=True)


from flask import Flask, render_template, request
from flask_socketio import SocketIO, join_room
import json
import uuid

# Create Flask app instance
app = Flask(__name__)

# Set the configuration value for MIN_NBR_TASKS
app.config['MIN_NBR_TASKS'] = 5  # Replace 5 with your desired value

socketio = SocketIO(app)

@app.route("/", methods=['GET'])
def index():
    return render_template('consumer.html')

def send_message(event, namespace, room, message):
    socketio.emit(event, message, namespace=namespace, room=room)

@app.before_request
def initialize_params():
    if 'uid' not in app.config:
        sid = str(uuid.uuid4())
        app.config['uid'] = sid
        print("initialize_params - Session ID stored =", sid)

@app.route('/consumetasks', methods=['POST'])
def consumetasks():
    if request.method == 'POST':
        data = request.json
        if data:
            print("Received Data = ", data)
            roomid = app.config['uid']
            var = json.dumps(data)
            send_message(event='msg', namespace='/collectHooks', room=roomid, message=var)
    return 'OK'

@socketio.on('connect', namespace='/collectHooks')
def socket_connect():
    print('Client Connected To NameSpace /collectHooks - ', request.sid)

@socketio.on('disconnect', namespace='/collectHooks')
def socket_disconnect():
    print('Client disconnected From NameSpace /collectHooks - ', request.sid)

@socketio.on('join_room', namespace='/collectHooks')
def on_room():
    if app.config['uid']:
        room = str(app.config['uid'])
        print(f"Socket joining room {room}")
        join_room(room)

@socketio.on_error_default
def error_handler(e):
    print(f"socket error: {e}, {str(request.event)}")

if __name__ == "__main__": 
    socketio.run(app, host='localhost', port=5001, debug=True)
