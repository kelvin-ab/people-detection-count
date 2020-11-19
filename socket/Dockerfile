FROM python:3.6-alpine

RUN pip install --upgrade pip && \
    pip install --no-cache-dir tornado
COPY . socket/
WORKDIR socket
ENTRYPOINT ["/usr/local/bin/python3", "./server.py"]
