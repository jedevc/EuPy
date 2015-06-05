# Python API for euphoria.io
An API that wraps sockets in a nice interface. Note: this library is only compatible with python3.

# How to set up
So, there is a setup.py file for installing and stuff but I have absolutely no idea how to use it. So, here are some simple setup instructions for those (like me) who don't care about the setup.py:

```bash
#If you don't want to use pip you can try downloading the client from the webpage at
#https://pypi.python.org/pypi/websocket-client
pip3 install websocket-client

git clone https://github.com/jedevc/euphoria-python.git

cd euphoria-python
python3 example.py
```

# Quick use
Create a new class which extends all the classes that you need to access from your bot. That's probably not enough to go on, unless you go digging into the code. So, there's a basic tutorial over at the wiki that you can look at and learn from. If you want an example, look in example.py for a basic bot that says hi.
