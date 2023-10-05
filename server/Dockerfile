# syntax=docker/dockerfile:1.4

FROM --platform=$BUILDPLATFORM python:3.7-alpine AS builder
EXPOSE 8000
WORKDIR /app
COPY requirements.txt /app

RUN apk --update add libxml2-dev libxslt-dev libffi-dev gcc musl-dev libgcc openssl-dev curl
RUN apk add jpeg-dev zlib-dev freetype-dev lcms2-dev openjpeg-dev tiff-dev tk-dev tcl-dev

RUN apk update && \
    pip install --upgrade distro-info && \
    pip3 install --upgrade pip==23.2.1 && \
    pip3 install -U -r requirements.txt --no-cache-dir

COPY . /app

# database migration commands here
RUN python3 manage.py makemigrations
RUN python3 manage.py migrate

ENTRYPOINT ["python3"]
CMD ["manage.py", "runserver", "0.0.0.0:8000"]

FROM builder as dev-envs
RUN apk update && \
    apk add git

RUN addgroup -S docker && \
    adduser -S --shell /bin/bash --ingroup docker vscode

# install Docker tools (cli, buildx, compose)
COPY --from=gloursdocker/docker / /
CMD ["manage.py", "runserver", "0.0.0.0:8000"]
