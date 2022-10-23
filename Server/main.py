import socketio

sio = socketio.Server()
app = socketio.WSGIApp(sio)

connected_users = {}

@sio.event
def connect(sid, environment, auth):
  print(sid, 'connected')
  print(auth)
  sio.save_session(sid, {'usr': auth['usr']})
  connected_users[auth['usr']] = {'sid': sid, 'kpub': auth['kpub']}
  sio.emit('message', {'msg': 'Welcome to the chat'}, to=sid)
  
@sio.event
def disconnect(sid):
  usr = sio.get_session(sid).get('usr')
  connected_users.pop(usr)
  sio.emit('disconnection', f'\n{usr} disconnected')

@sio.event
def send_message(sid, data):
  if data['send_to'] and data['send_to'] in connected_users:
    sio.emit('message', {'msg': data['msg']}, to=connected_users[data['send_to']]['sid'])
  else:
    sio.emit('message', {'msg': data['msg']})
