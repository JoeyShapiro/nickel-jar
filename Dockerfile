FROM python:3.8-slim

RUN mkdir -p /app/data
RUN apt-get update
RUN pip install --upgrade pip
RUN pip install discord.py mysql-connector-python

COPY nickel-jar.py /app/nickel-jar.py

WORKDIR /app

ENTRYPOINT [ "python", "/app/nickel-jar.py" ]
