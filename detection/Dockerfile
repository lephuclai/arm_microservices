FROM ubuntu:20.04

RUN export LC_CTYPE=en_US.UTF-8

RUN apt-get update && \
    apt-get install sudo && \
    apt-get install -y software-properties-common && \
    add-apt-repository -y ppa:deadsnakes/ppa && \
    apt-get update && \
    apt-get install wget && \
    apt install -y python3.8

RUN apt-get update && apt-get install curl -y
RUN apt install python3-pip -y
RUN python3 -m pip install --upgrade pip
RUN apt-get update && apt-get install ffmpeg libsm6 libxext6  -y

RUN mkdir /yolo && \
    mkdir /data && \
	mkdir /conf && \
    pip3 install flask flask_pymongo werkzeug opencv-python numpy

COPY yolov3-tiny.cfg /yolo/	
COPY yolov3-tiny.txt /yolo/	
COPY yolov3-tiny.weights /yolo/
COPY app.py /yolo/
COPY startup.sh /

RUN chmod +x /startup.sh

EXPOSE 5000

ENTRYPOINT ["/startup.sh"]