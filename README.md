# EuPy by @jedevc
An API that wraps sockets in a nice interface and provides methods for sending and receiving packets from euphoria.

## How to set up
So, there is a setup.py file for installing which works as follows:

```bash
python3 setup.py install
```

But if you don't want to actually install the library you can just download it like so:
```bash
#Install dependencies
pip3 install websocket-client

#Clone the repo
git clone https://github.com/jedevc/euphoria-python.git

#Navigate to the directory and compress the files into one file
cd eupy
python3 min.py > eupy.py
```

## Quick use
Create a new class which extends all the classes that you need to access from your bot. That's probably not enough to go on, unless you go digging into the code. So, there's a basic tutorial over at the wiki that you can look at and learn from. You can look in the examples folder for a few demos of what you might want to do.
