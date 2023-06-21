# syntax=docker/dockerfile:1

FROM python:3.9-slim-buster

WORKDIR /usr/src/hypercube

ENV APP_NAME=hypercube
ENV LOCAL_HOST=0.0.0.0
ENV INIT_PORT=8880
ENV HOP_SERVER_PORT=6000
#ENV NODE_PORT=8881
#ENV HYPERCUBE_SIZE=3
#ENV SUPERSET_THRESHOLD=10

COPY requirements.txt requirements.txt
RUN pip3 install -r requirements.txt

#EXPOSE 5000

COPY ./src .

CMD ["sh", "-c", "python3 server.py $NODE_PORT"]