from operator import truediv
import sys
import socketio
import RSA as rsa
from random import choice
# sio = socketio.Client(logger=True, engineio_logger=True)
sio = socketio.Client()

p = 2 ** 1024 - 105 
q = 2 ** 1023 + 1155

K_pub, K_priv = rsa.RSA(p, q)
K_pub_b = None

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
def receive_public_keys(kpub):
  global K_pub_b
  K_pub_b = kpub['kpub']

@sio.event
def message(data):
  #Recover encrypted blocks
  sliced = rsa.slicer_inv(data['msg'])
  sliced_sig = rsa.slicer_inv(data['signature'])
  is_valid = rsa.ecb_signature_validation(sliced, sliced_sig, K_pub_b[data['from']]['kpub'])
  
  #Check the integrity of the message
  if is_valid:
    print('El mensaje es válido!')
    print('Descifrando!')
    #Dectypt the obtained blocks
    clear_text = rsa.ecb_decryption(sliced, K_pub, K_priv)
    print("Obtained Message:\n", clear_text, '\n')
  else:
    print('Ocurrió algo con el mensaje...')

@sio.event
def disconnection(data):
  print(data)

def menu():
    conn = True
    while conn:
        option = input('\nWhat you want to do? \n1. Send a msj \n2. Get your kpub \n3. Close conn \nOption: ')
        if option == '1':
            send_to = input('Send to: ')
            if send_to in K_pub_b:
              msg = input('Put here your message: ')
              message, signature = rsa.ecb(msg, K_pub, K_pub_b[send_to]['kpub'], K_priv)
              should_modify = choice([True, False])
              if should_modify:
                print('Modifying the message...')
                original_to_modify = choice(['0', '1'])
                modify_to = '1' if original_to_modify == '0' else '0'
                sio.emit('send_message', {'msg': message.replace(original_to_modify, modify_to), 'signature': signature, 'send_to': send_to})
              else:
                sio.emit('send_message', {'msg': message, 'signature': signature, 'send_to': send_to})
                
        elif option == '2':
            print(K_pub)
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
  global K_priv, K_pub, p, q
  print('connecting...', args[1])
  sio.connect(url, auth={'usr': args[1],'kpub': K_pub})
  sio.wait()

if __name__ == '__main__':
  main(sys.argv if len(sys.argv) > 1 else None)