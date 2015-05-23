# Python API for euphoria.io
An API that wraps sockets in a nice interface. Note: this library is only compatible with python3.

# How to set up
At the moment, there are no setup things. So, until I make one, here are some basic instructions on how to download this library and run the example:

```bash
#If you don't want to use pip you can try downloading the client from the webpage at
#https://pypi.python.org/pypi/websocket-client
pip3 install websocket-client

git clone https://github.com/jedevc/euphoria-python.git

cd euphoria-python
python3 example.py
```

# Quick use
Extend one of the components to do what you want. Choose the one that is closed in functionality to what you want. Then add that component and any other components that you need to the room. Hopefully my code is clean enough to make it simple enough to read.

For a basic example of a hello bot, look in example.py.
