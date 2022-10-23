# RSA-communication-socketio
This is a RSA Communicatio implementation using websockets from Socketio in python without any UI.

To run this code:
First of all download/clone the repository on your desired directory, then you have to install some dependencies if you dont have them:

```Batchfile
  pip install "python-socketio" && pip install "python-socketio[client]" && pip install "gunicorn"
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
