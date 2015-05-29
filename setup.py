from distutils.core import setup

setup(name='euphoria-python',
        version='1.0',
        description='An API to interact with the chatrooms at euphoria.io',
        author='Justin Chadwell',
        author_email='jedevc@gmail.com',
        url='https://github.com/jedevc/euphoria-python',
        license='MIT',
        packages=['euphoria'],
        install_requires=['websocket-client']
)