FROM alpine:3.9

MAINTAINER pokemonpvp.club

RUN apk update && \
    apk add python3 python3-dev build-base zlib-dev jpeg-dev

WORKDIR pokemonpvp.club

COPY . .
CMD ["./run.sh"]
EXPOSE 8000/tcp

RUN pip3 install -r requirements.txt && \
    apk del build-base

