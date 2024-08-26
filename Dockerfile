FROM python:3.11-alpine

USER root

WORKDIR /app

COPY /api ./api
COPY /assets ./assets
COPY pyproject.toml .
COPY Makefile .

RUN apk update && apk add git make

RUN make

EXPOSE 8000
ENV LISTEN_PORT = 8000

CMD ["fastapi", "run", "api/main.py"]