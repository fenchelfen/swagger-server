FROM python:3-alpine

RUN mkdir -p /usr/src/app
WORKDIR /usr/src/app

COPY requirements.txt /usr/src/app/

RUN pip3 install --no-cache-dir -r requirements.txt

COPY . /usr/src/app

EXPOSE 80

RUN apk add redis git build-base
RUN git clone https://github.com/RedisLabsModules/rejson.git ; \
    cd rejson ; \
    make ; \
    mkdir -p /etc/redis/modules ; \
    cp ./src/rejson.so /etc/redis/modules


ENTRYPOINT /usr/bin/redis-server --loadmodule /etc/redis/modules/rejson.so --daemonize yes && python3 -m swagger_server