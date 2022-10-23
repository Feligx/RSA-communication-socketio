from operator import truediv
import sys
import socketio

# sio = socketio.Client(logger=True, engineio_logger=True)
sio = socketio.Client()

akpriv = None
akpub = None
bkpub = akpriv

@sio.event
def connect():
  print('connected')
  menu()
#   sio.emit('send_message', {'greeting': 'welcome'})
  

@sio.event
def connect_error(e):
  print(e)

@sio.event
def disconnect():
  print('Disconnected! Bye...')

@sio.event
def message(data):
    print('\nreceived message: ' + data['msg'] + '\n')

@sio.event
def disconnection(data):
  print(data)

def menu():
    conn = True
    while conn:
        option = input('\nWhat you want to do? \n1. Send a msj \n2. Get your kpub \n3. Close conn \nOption: ')
        if option == '1':
            send_to = input('Send to: ')
            msg = input('Put here your message: ')
            sio.emit('send_message', {'msg': msg, 'send_to': send_to})
        elif option == '2':
            print(akpub)
            menu()
        elif option == '3':
            conn = False
            sio.disconnect()
        else:
            print('That is not a valid option, please choose one of the available options...')
    
    # sio.disconnect()

def main(args):
  url = 'http://127.0.0.1:8000'
  print(args)
  global akpub
  akpub = args[1]
  print('connecting...', akpub)
  sio.connect(url, auth={'usr': args[2],'kpub': akpub})
  sio.wait()

if __name__ == '__main__':
  main(sys.argv if len(sys.argv) > 1 else None)
