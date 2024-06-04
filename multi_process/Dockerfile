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
RUN apt-get update && apt-get install gnupg wget -y

RUN wget -qO - https://www.mongodb.org/static/pgp/server-4.4.asc | sudo apt-key add -
RUN echo "deb [ arch=amd64,arm64 ] https://repo.mongodb.org/apt/ubuntu focal/mongodb-org/4.4 multiverse" | sudo tee /etc/apt/sources.list.d/mongodb-org-4.4.list
RUN apt-get update
RUN apt-get install -y mongodb-org=4.4.18 mongodb-org-server=4.4.18 mongodb-org-shell=4.4.18 mongodb-org-mongos=4.4.18 mongodb-org-tools=4.4.18
RUN rm -rf /var/lib/apt/lists/*

WORKDIR /var/www/
ADD . /var/www/

RUN pip3 install -r requirements.txt

RUN mkdir /data
RUN mkdir /data/db

EXPOSE 5500
EXPOSE 27017

COPY startup.sh /
RUN chmod +x /startup.sh

ENTRYPOINT ["/startup.sh"]

