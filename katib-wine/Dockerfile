FROM ubuntu:16.04

RUN apt-get update && \
    apt-get install -y wget python3-dev gcc && \
    wget https://bootstrap.pypa.io/get-pip.py && \
    python3 get-pip.py

RUN pip3 install mlflow && \
    pip3 install sklearn && \
    pip3 install pandas && \
    pip3 install numpy

ADD . /katib
WORKDIR /katib


ENTRYPOINT ["python3", "/katib/katib.py"]
