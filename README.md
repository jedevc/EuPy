# Python API for euphoria.io
An API that wraps sockets in a nice interface. Note: this library is only compatible with python3 at the moment. I will definitely work on making it available for python2 at some point in the future.

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
Extend one of the Room classes, prefereably the one that has the closest functionality to what you need. Then simply override the methods of of that class. Hopefully my code is clean enough to make it simple enough to read.

For a basic example of a hello bot, look in example.py.
