FROM python:3.8-slim-buster

LABEL org.opencontainers.image.source=https://github.com/masluse/DNSKEY-to-DS

WORKDIR /app

RUN apt-get update && apt-get install -y dnsutils

COPY requirements.txt requirements.txt
RUN pip3 install -r requirements.txt

COPY . .

CMD [ "python3", "-m" , "flask", "run", "--host=0.0.0.0"]
