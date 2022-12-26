FROM python:3.9-alpine

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

WORKDIR /app

RUN apk --update add
RUN apk add gcc libc-dev libffi-dev jpeg-dev zlib-dev libjpeg libxml2-dev libxslt-dev openssl musl-dev openssl-dev cargo python3-dev
RUN apk add postgresql-dev
RUN apk add tk-dev
RUN apk add build-base

RUN apk add --no-cache tzdata
ENV TZ Asia/Almaty

RUN pip install --upgrade pip

COPY ./requirements.txt .
COPY ./entrypoint.sh .

RUN pip install pip --upgrade
RUN pip install -r requirements.txt
RUN pip install pyopenssl --upgrade

RUN chmod +x entrypoint.sh

COPY . .

ENTRYPOINT ["sh", "/app/entrypoint.sh"]
