FROM python

ADD . /code/EuPy
WORKDIR /code/EuPy
RUN python3 setup.py install
