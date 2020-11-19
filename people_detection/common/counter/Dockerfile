FROM python:3.6-alpine

RUN pip install --upgrade pip && \
    pip install --no-cache-dir numpy

RUN mkdir counter
COPY common/counter/*.py counter/
WORKDIR  counter
ENTRYPOINT ["/usr/local/bin/python3", "./obj_counter.py"]

