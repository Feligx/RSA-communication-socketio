# RSA-communication-socketio
This is a RSA Communicatio implementation using websockets from Socketio in python without any UI.

## Specs:
* Keys of 2048 bits for both Encryption and Signature.
* ECB encryption mode (Although this could be improved).
* Supports `n` length of message as input.
* Fast Encpryption and Decryption.
* Implemented as websockets, could be easily changed for a web application usage, or for remote comms with a dedicated server and domain.
* Supports as many users as needed, but comms are 1-1 private.

## Running the code:
First of all download/clone the repository on your desired directory, then you have to install some dependencies if you dont have them:

```Batchfile
  pip install "python-socketio" "python-socketio[client]" "gunicorn"
```

* Server:
  To run the server move to the server folder, then run in a command line 
  
  ```Batchfile
    gunicorn --threads 50 main:app
  ```
  
  and it should start in port 8000 over the localhost

* Client:
  Now to run the client, on a different command line, go to the client folder and run 
  ```Batchfile
    python3 main.py <public_key> <username>
  ```
  > Note: Sometimes python3 commando will not be avialable on your machine, check if `py`, `python`or `py3`are available if none of them are, then check if you have a python distribution installed and if you have check that the PATH of the distribution is correct.
  
  This will start a new client on the chat, if you want two or more just open more command lines and run the same command with different usernames.
