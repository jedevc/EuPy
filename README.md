# [Euphoria](euphoria.io) API by @jedevc
An API that wraps sockets in a nice interface and provides methods for sending and receiving packets from euphoria.

## How to set up
So, there is a setup.py file for installing and stuff but I have absolutely no idea how to use it. So, here are some simple setup instructions for those (like me) who don't care about the setup.py:

```bash
#If you don't want to use pip you can try downloading the client from the webpage at
#https://pypi.python.org/pypi/websocket-client
pip3 install websocket-client

#Clone the repo
git clone https://github.com/jedevc/euphoria-python.git

#Navigate to the directory and run the example
cd euphoria-python
python3 examples/hello.py
```

## Quick use
Create a new class which extends all the classes that you need to access from your bot. That's probably not enough to go on, unless you go digging into the code. So, there's a basic tutorial over at the wiki that you can look at and learn from. You can look in the examples folder for a few demos of what you might want to do.
