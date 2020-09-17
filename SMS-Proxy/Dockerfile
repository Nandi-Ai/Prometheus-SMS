FROM python:3.7.4-alpine3.10

COPY ./requirements.txt /app/requirements.txt
COPY ./sms.py /app/sms.py
COPY ./config /app/config
WORKDIR /app
RUN apk add --update gcc linux-headers musl-dev libffi-dev py-cryptography openssl-dev
RUN pip3 install -r requirements.txt
EXPOSE 8000
CMD gunicorn -b 0.0.0.0:8000 sms:app
